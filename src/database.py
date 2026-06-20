import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "gestao_vinicius.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS frentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            limite_dias INTEGER DEFAULT 7,
            status TEXT DEFAULT 'ativa',
            criado_em TEXT DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS semanas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_inicio TEXT NOT NULL UNIQUE,
            data_fim TEXT NOT NULL,
            foco_principal TEXT,
            tempo_livre_horas REAL DEFAULT 0,
            observacoes TEXT,
            criado_em TEXT DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semana_id INTEGER NOT NULL,
            frente_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            tempo_planejado_min INTEGER DEFAULT 0,
            tempo_realizado_min INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pendente',
            criado_em TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (semana_id) REFERENCES semanas(id),
            FOREIGN KEY (frente_id) REFERENCES frentes(id)
        );

        CREATE TABLE IF NOT EXISTS financas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semana_id INTEGER NOT NULL UNIQUE,
            gasto_semana REAL DEFAULT 0,
            saldo_atual REAL DEFAULT 0,
            observacoes TEXT,
            registrado_em TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (semana_id) REFERENCES semanas(id)
        );

        CREATE TABLE IF NOT EXISTS agenda_manual (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semana_id INTEGER NOT NULL,
            dia_semana TEXT NOT NULL,
            hora_inicio TEXT,
            hora_fim TEXT,
            descricao TEXT NOT NULL,
            criado_em TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (semana_id) REFERENCES semanas(id)
        );

        CREATE TABLE IF NOT EXISTS revisao_semanal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semana_id INTEGER NOT NULL UNIQUE,
            o_que_foi_bem TEXT,
            o_que_melhorar TEXT,
            aprendizados TEXT,
            nota_semana INTEGER,
            revisado_em TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (semana_id) REFERENCES semanas(id)
        );
    """)

    conn.commit()
    conn.close()
