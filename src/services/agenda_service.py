from src.database import get_connection

DIAS_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


def listar_agenda(semana_id: int) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM agenda_manual WHERE semana_id = ? ORDER BY dia_semana, hora_inicio",
        (semana_id,),
    )
    agenda = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return agenda


def adicionar_item(semana_id: int, dia: str, hora_inicio: str,
                   hora_fim: str, descricao: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO agenda_manual (semana_id, dia_semana, hora_inicio, hora_fim, descricao)
        VALUES (?, ?, ?, ?, ?)
        """,
        (semana_id, dia, hora_inicio or None, hora_fim or None, descricao.strip()),
    )
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return item_id


def excluir_item(item_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM agenda_manual WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
