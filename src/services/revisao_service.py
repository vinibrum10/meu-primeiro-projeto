from src.database import get_connection


def obter_revisao(semana_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM revisao_semanal WHERE semana_id = ?", (semana_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def salvar_revisao(semana_id: int, bem: str, melhorar: str, aprendizados: str, nota: int):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO revisao_semanal (semana_id, o_que_foi_bem, o_que_melhorar, aprendizados, nota_semana)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(semana_id) DO UPDATE SET
            o_que_foi_bem = excluded.o_que_foi_bem,
            o_que_melhorar = excluded.o_que_melhorar,
            aprendizados = excluded.aprendizados,
            nota_semana = excluded.nota_semana,
            revisado_em = datetime('now', 'localtime')
        """,
        (semana_id, bem.strip(), melhorar.strip(), aprendizados.strip(), nota),
    )
    conn.commit()
    conn.close()
