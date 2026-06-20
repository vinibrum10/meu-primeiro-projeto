from src.database import get_connection

FRENTES_INICIAIS = [
    {"nome": "Carreira / EUA", "limite_dias": 7},
    {"nome": "Doutorado", "limite_dias": 7},
    {"nome": "Inglês / TOEFL", "limite_dias": 7},
    {"nome": "Finanças", "limite_dias": 7},
    {"nome": "Programação / Tecnologia", "limite_dias": 7},
    {"nome": "Rotina / Equilíbrio", "limite_dias": 7},
    {"nome": "Trabalho / Aulas", "limite_dias": 7},
    {"nome": "Acompanhamentos", "limite_dias": 14},
]


def seed_frentes():
    conn = get_connection()
    cursor = conn.cursor()
    for frente in FRENTES_INICIAIS:
        cursor.execute(
            "INSERT OR IGNORE INTO frentes (nome, limite_dias) VALUES (?, ?)",
            (frente["nome"], frente["limite_dias"]),
        )
    conn.commit()
    conn.close()


def run_seed():
    seed_frentes()
