from src.database import get_connection
from src.calculations import calcular_divida_atencao


def listar_frentes(apenas_ativas: bool = False) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    if apenas_ativas:
        cursor.execute("SELECT * FROM frentes WHERE status = 'ativa' ORDER BY nome")
    else:
        cursor.execute("SELECT * FROM frentes ORDER BY nome")
    frentes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return frentes


def obter_frente(frente_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM frentes WHERE id = ?", (frente_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def criar_frente(nome: str, limite_dias: int = 7) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO frentes (nome, limite_dias) VALUES (?, ?)",
        (nome.strip(), limite_dias),
    )
    frente_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return frente_id


def atualizar_frente(frente_id: int, nome: str, limite_dias: int, status: str):
    conn = get_connection()
    conn.execute(
        "UPDATE frentes SET nome = ?, limite_dias = ?, status = ? WHERE id = ?",
        (nome.strip(), limite_dias, status, frente_id),
    )
    conn.commit()
    conn.close()


def obter_dividas_atencao(semanas_recentes: int = 8) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM frentes ORDER BY nome")
    frentes = [dict(row) for row in cursor.fetchall()]

    resultado = []
    for frente in frentes:
        cursor.execute(
            """
            SELECT MAX(t.criado_em) as ultima
            FROM tarefas t
            JOIN semanas s ON t.semana_id = s.id
            WHERE t.frente_id = ?
              AND t.status = 'concluida'
            ORDER BY t.criado_em DESC
            LIMIT 1
            """,
            (frente["id"],),
        )
        row = cursor.fetchone()
        ultima_atividade = row["ultima"] if row and row["ultima"] else None

        nivel = calcular_divida_atencao(
            ultima_atividade=ultima_atividade,
            limite_dias=frente["limite_dias"],
            status_frente=frente["status"],
        )
        resultado.append({
            **frente,
            "ultima_atividade": ultima_atividade,
            "divida": nivel,
        })

    conn.close()
    return resultado
