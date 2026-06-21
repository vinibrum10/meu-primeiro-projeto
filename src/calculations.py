from datetime import datetime, date, timedelta
from typing import Optional


def calcular_divida_atencao(
    ultima_atividade: Optional[str],
    limite_dias: int,
    status_frente: str,
) -> str:
    """
    Retorna o nível de dívida de atenção para uma frente de vida.

    Regras:
    - pausada: nenhum alerta
    - ok: dentro do limite
    - atenção: passou do limite
    - crítico: passou do dobro do limite
    """
    if status_frente == "pausada":
        return "pausada"

    if ultima_atividade is None:
        return "crítico"

    try:
        if isinstance(ultima_atividade, str):
            ultima = datetime.strptime(ultima_atividade[:10], "%Y-%m-%d").date()
        else:
            ultima = ultima_atividade
    except (ValueError, TypeError):
        return "crítico"

    dias_passados = (date.today() - ultima).days

    if dias_passados <= limite_dias:
        return "ok"
    elif dias_passados <= limite_dias * 2:
        return "atenção"
    else:
        return "crítico"


def calcular_progresso_semana(tarefas: list) -> dict:
    """
    Calcula métricas de progresso de uma semana.

    tarefas: lista de dicts com chaves:
        - status: 'pendente', 'concluida', 'cancelada'
        - tempo_planejado_min: int
        - tempo_realizado_min: int
        - frente_id: int
    """
    total = len(tarefas)
    concluidas = sum(1 for t in tarefas if t["status"] == "concluida")
    canceladas = sum(1 for t in tarefas if t["status"] == "cancelada")
    pendentes = total - concluidas - canceladas

    tempo_planejado = sum(t.get("tempo_planejado_min", 0) or 0 for t in tarefas)
    tempo_realizado = sum(t.get("tempo_realizado_min", 0) or 0 for t in tarefas)

    frentes_ativas = set(
        t["frente_id"] for t in tarefas if t["status"] != "cancelada"
    )

    percentual = round((concluidas / total * 100) if total > 0 else 0, 1)

    return {
        "total": total,
        "concluidas": concluidas,
        "pendentes": pendentes,
        "canceladas": canceladas,
        "percentual_concluido": percentual,
        "tempo_planejado_min": tempo_planejado,
        "tempo_realizado_min": tempo_realizado,
        "frentes_com_acao": len(frentes_ativas),
    }


def calcular_financas(registros: list) -> dict:
    """
    Calcula métricas financeiras a partir de uma lista de registros semanais.

    registros: lista de dicts ordenada por data (mais recente por último).
        - gasto_semana: float
        - saldo_atual: float
        - registrado_em: str (data ISO)
    """
    if not registros:
        return {
            "gasto_semana_atual": 0.0,
            "saldo_atual": 0.0,
            "variacao_saldo": None,
            "media_gasto_mensal": 0.0,
        }

    atual = registros[-1]
    gasto_atual = atual.get("gasto_semana", 0) or 0
    saldo_atual = atual.get("saldo_atual", 0) or 0

    variacao = None
    if len(registros) >= 2:
        anterior = registros[-2]
        saldo_anterior = anterior.get("saldo_atual", 0) or 0
        variacao = round(saldo_atual - saldo_anterior, 2)

    hoje = date.today()
    primeiro_dia_mes = hoje.replace(day=1)

    gastos_mes = [
        r.get("gasto_semana", 0) or 0
        for r in registros
        if _data_no_mes(r.get("registrado_em", ""), primeiro_dia_mes)
    ]

    media_mensal = round(sum(gastos_mes) / len(gastos_mes), 2) if gastos_mes else 0.0

    return {
        "gasto_semana_atual": round(gasto_atual, 2),
        "saldo_atual": round(saldo_atual, 2),
        "variacao_saldo": variacao,
        "media_gasto_mensal": media_mensal,
    }


def _data_no_mes(data_str: str, primeiro_dia_mes: date) -> bool:
    try:
        d = datetime.strptime(data_str[:10], "%Y-%m-%d").date()
        return d >= primeiro_dia_mes
    except (ValueError, TypeError):
        return False


def minutos_para_horas(minutos: int) -> str:
    if not minutos:
        return "0h 0min"
    h = minutos // 60
    m = minutos % 60
    return f"{h}h {m}min"


def data_inicio_semana_atual() -> date:
    hoje = date.today()
    return hoje - timedelta(days=hoje.weekday())


def data_fim_semana(data_inicio: date) -> date:
    return data_inicio + timedelta(days=6)
