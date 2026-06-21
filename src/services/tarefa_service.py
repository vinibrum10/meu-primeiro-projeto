from src.database import get_connection
from src.calculations import calcular_progresso_semana


def listar_tarefas_semana(semana_id: int) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT t.*, f.nome as frente_nome, f.status as frente_status
        FROM tarefas t
        JOIN frentes f ON t.frente_id = f.id
        WHERE t.semana_id = ?
        ORDER BY f.nome, t.criado_em
        """,
        (semana_id,),
    )
    tarefas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tarefas


def criar_tarefa(semana_id: int, frente_id: int, descricao: str,
                 tempo_planejado_min: int = 0) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO tarefas (semana_id, frente_id, descricao, tempo_planejado_min)
        VALUES (?, ?, ?, ?)
        """,
        (semana_id, frente_id, descricao.strip(), tempo_planejado_min),
    )
    tarefa_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return tarefa_id


def atualizar_status_tarefa(tarefa_id: int, status: str, tempo_realizado_min: int = 0):
    conn = get_connection()
    conn.execute(
        "UPDATE tarefas SET status = ?, tempo_realizado_min = ? WHERE id = ?",
        (status, tempo_realizado_min, tarefa_id),
    )
    conn.commit()
    conn.close()


def excluir_tarefa(tarefa_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    conn.commit()
    conn.close()


def progresso_semana(semana_id: int) -> dict:
    tarefas = listar_tarefas_semana(semana_id)
    return calcular_progresso_semana(tarefas)
