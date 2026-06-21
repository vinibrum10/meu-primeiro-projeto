import pytest
from datetime import date, timedelta
from src.calculations import (
    calcular_divida_atencao,
    calcular_progresso_semana,
    calcular_financas,
    minutos_para_horas,
    data_inicio_semana_atual,
    data_fim_semana,
)


class TestDividaAtencao:
    def test_pausada_nao_gera_alerta(self):
        resultado = calcular_divida_atencao("2020-01-01", 7, "pausada")
        assert resultado == "pausada"

    def test_sem_atividade_critico(self):
        resultado = calcular_divida_atencao(None, 7, "ativa")
        assert resultado == "crítico"

    def test_dentro_limite_ok(self):
        hoje = date.today()
        ultima = (hoje - timedelta(days=3)).isoformat()
        resultado = calcular_divida_atencao(ultima, 7, "ativa")
        assert resultado == "ok"

    def test_passou_limite_atencao(self):
        hoje = date.today()
        ultima = (hoje - timedelta(days=10)).isoformat()
        resultado = calcular_divida_atencao(ultima, 7, "ativa")
        assert resultado == "atenção"

    def test_passou_dobro_critico(self):
        hoje = date.today()
        ultima = (hoje - timedelta(days=15)).isoformat()
        resultado = calcular_divida_atencao(ultima, 7, "ativa")
        assert resultado == "crítico"

    def test_exatamente_no_limite_ok(self):
        hoje = date.today()
        ultima = (hoje - timedelta(days=7)).isoformat()
        resultado = calcular_divida_atencao(ultima, 7, "ativa")
        assert resultado == "ok"

    def test_data_invalida_critico(self):
        resultado = calcular_divida_atencao("data-invalida", 7, "ativa")
        assert resultado == "crítico"

    def test_limite_personalizado(self):
        hoje = date.today()
        ultima = (hoje - timedelta(days=20)).isoformat()
        resultado = calcular_divida_atencao(ultima, 14, "ativa")
        assert resultado == "atenção"


class TestProgressoSemana:
    def _tarefa(self, status, planejado=60, realizado=0, frente_id=1):
        return {
            "status": status,
            "tempo_planejado_min": planejado,
            "tempo_realizado_min": realizado,
            "frente_id": frente_id,
        }

    def test_sem_tarefas(self):
        prog = calcular_progresso_semana([])
        assert prog["total"] == 0
        assert prog["percentual_concluido"] == 0
        assert prog["frentes_com_acao"] == 0

    def test_todas_concluidas(self):
        tarefas = [self._tarefa("concluida") for _ in range(5)]
        prog = calcular_progresso_semana(tarefas)
        assert prog["total"] == 5
        assert prog["concluidas"] == 5
        assert prog["percentual_concluido"] == 100.0

    def test_misto(self):
        tarefas = [
            self._tarefa("concluida", frente_id=1),
            self._tarefa("concluida", frente_id=2),
            self._tarefa("pendente", frente_id=2),
            self._tarefa("cancelada", frente_id=3),
        ]
        prog = calcular_progresso_semana(tarefas)
        assert prog["total"] == 4
        assert prog["concluidas"] == 2
        assert prog["canceladas"] == 1
        assert prog["percentual_concluido"] == 50.0
        assert prog["frentes_com_acao"] == 2

    def test_tempo_somado(self):
        tarefas = [
            self._tarefa("concluida", planejado=60, realizado=45),
            self._tarefa("pendente", planejado=90, realizado=30),
        ]
        prog = calcular_progresso_semana(tarefas)
        assert prog["tempo_planejado_min"] == 150
        assert prog["tempo_realizado_min"] == 75

    def test_cancelada_nao_conta_em_frentes(self):
        tarefas = [
            self._tarefa("cancelada", frente_id=1),
            self._tarefa("concluida", frente_id=2),
        ]
        prog = calcular_progresso_semana(tarefas)
        assert prog["frentes_com_acao"] == 1


class TestFinancas:
    def _registro(self, gasto, saldo, data="2024-06-15"):
        return {"gasto_semana": gasto, "saldo_atual": saldo, "registrado_em": data}

    def test_sem_registros(self):
        resultado = calcular_financas([])
        assert resultado["gasto_semana_atual"] == 0.0
        assert resultado["saldo_atual"] == 0.0
        assert resultado["variacao_saldo"] is None

    def test_um_registro(self):
        registros = [self._registro(500, 3000)]
        resultado = calcular_financas(registros)
        assert resultado["gasto_semana_atual"] == 500
        assert resultado["saldo_atual"] == 3000
        assert resultado["variacao_saldo"] is None

    def test_dois_registros_variacao(self):
        registros = [
            self._registro(400, 2000),
            self._registro(600, 1400),
        ]
        resultado = calcular_financas(registros)
        assert resultado["gasto_semana_atual"] == 600
        assert resultado["saldo_atual"] == 1400
        assert resultado["variacao_saldo"] == -600

    def test_variacao_positiva(self):
        registros = [
            self._registro(0, 2000),
            self._registro(0, 2500),
        ]
        resultado = calcular_financas(registros)
        assert resultado["variacao_saldo"] == 500


class TestMinutosParaHoras:
    def test_zero(self):
        assert minutos_para_horas(0) == "0h 0min"

    def test_menos_de_hora(self):
        assert minutos_para_horas(45) == "0h 45min"

    def test_exatamente_uma_hora(self):
        assert minutos_para_horas(60) == "1h 0min"

    def test_hora_e_meia(self):
        assert minutos_para_horas(90) == "1h 30min"

    def test_nenhum(self):
        assert minutos_para_horas(None) == "0h 0min"


class TestDatasSemana:
    def test_inicio_semana_e_segunda(self):
        inicio = data_inicio_semana_atual()
        assert inicio.weekday() == 0

    def test_fim_semana_e_domingo(self):
        inicio = data_inicio_semana_atual()
        fim = data_fim_semana(inicio)
        assert fim.weekday() == 6
        assert (fim - inicio).days == 6
