from src.database import get_connection
from src.calculations import calcular_financas


def obter_financas_semana(semana_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM financas WHERE semana_id = ?", (semana_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def registrar_financas(semana_id: int, gasto: float, saldo: float, obs: str = "") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO financas (semana_id, gasto_semana, saldo_atual, observacoes)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(semana_id) DO UPDATE SET
            gasto_semana = excluded.gasto_semana,
            saldo_atual = excluded.saldo_atual,
            observacoes = excluded.observacoes,
            registrado_em = datetime('now', 'localtime')
        """,
        (semana_id, gasto, saldo, obs.strip()),
    )
    registro_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return registro_id


def metricas_financeiras() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT f.*, s.data_inicio
        FROM financas f
        JOIN semanas s ON f.semana_id = s.id
        ORDER BY s.data_inicio ASC
        """
    )
    registros = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return calcular_financas(registros)


def historico_financas(limite: int = 12) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT f.*, s.data_inicio, s.data_fim
        FROM financas f
        JOIN semanas s ON f.semana_id = s.id
        ORDER BY s.data_inicio DESC
        LIMIT ?
        """,
        (limite,),
    )
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado
