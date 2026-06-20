from src.database import get_connection
from src.calculations import data_inicio_semana_atual, data_fim_semana


def listar_semanas() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM semanas ORDER BY data_inicio DESC")
    semanas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return semanas


def obter_semana(semana_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM semanas WHERE id = ?", (semana_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def obter_semana_atual() -> dict | None:
    inicio = data_inicio_semana_atual()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM semanas WHERE data_inicio = ?",
        (inicio.isoformat(),),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def criar_semana_atual(foco: str = "", tempo_livre: float = 0.0, obs: str = "") -> int:
    inicio = data_inicio_semana_atual()
    fim = data_fim_semana(inicio)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR IGNORE INTO semanas (data_inicio, data_fim, foco_principal, tempo_livre_horas, observacoes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (inicio.isoformat(), fim.isoformat(), foco.strip(), tempo_livre, obs.strip()),
    )
    conn.commit()

    cursor.execute("SELECT id FROM semanas WHERE data_inicio = ?", (inicio.isoformat(),))
    semana_id = cursor.fetchone()["id"]
    conn.close()
    return semana_id


def criar_semana(data_inicio_str: str, foco: str = "", tempo_livre: float = 0.0, obs: str = "") -> int:
    from datetime import date, timedelta
    inicio = date.fromisoformat(data_inicio_str)
    fim = inicio + timedelta(days=6)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR IGNORE INTO semanas (data_inicio, data_fim, foco_principal, tempo_livre_horas, observacoes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (inicio.isoformat(), fim.isoformat(), foco.strip(), tempo_livre, obs.strip()),
    )
    conn.commit()
    cursor.execute("SELECT id FROM semanas WHERE data_inicio = ?", (inicio.isoformat(),))
    semana_id = cursor.fetchone()["id"]
    conn.close()
    return semana_id


def atualizar_semana(semana_id: int, foco: str, tempo_livre: float, obs: str):
    conn = get_connection()
    conn.execute(
        "UPDATE semanas SET foco_principal = ?, tempo_livre_horas = ?, observacoes = ? WHERE id = ?",
        (foco.strip(), tempo_livre, obs.strip(), semana_id),
    )
    conn.commit()
    conn.close()
