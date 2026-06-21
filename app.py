import streamlit as st
from src.database import init_db
from src.seed import run_seed

st.set_page_config(
    page_title="Gestão Vinicius",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
run_seed()

PAGINAS = {
    "📋 Painel da Semana": "painel_semana",
    "✅ Tarefas Semanais": "tarefas_semanais",
    "🎯 Frentes de Vida": "frentes_de_vida",
    "💰 Finanças": "financas",
    "📈 Progresso": "progresso",
    "🌙 Revisão de Domingo": "revisao_domingo",
    "📅 Agenda Manual": "agenda_manual",
}

with st.sidebar:
    st.title("🎯 Gestão Vinicius")
    st.caption("Planejamento semanal pessoal")
    st.divider()
    pagina_escolhida = st.radio("Navegação", list(PAGINAS.keys()), label_visibility="collapsed")
    st.divider()
    st.caption("v1.0 — MVP pessoal")

modulo_nome = PAGINAS[pagina_escolhida]

if modulo_nome == "painel_semana":
    from src.pages.painel_semana import render
elif modulo_nome == "tarefas_semanais":
    from src.pages.tarefas_semanais import render
elif modulo_nome == "frentes_de_vida":
    from src.pages.frentes_de_vida import render
elif modulo_nome == "financas":
    from src.pages.financas import render
elif modulo_nome == "progresso":
    from src.pages.progresso import render
elif modulo_nome == "revisao_domingo":
    from src.pages.revisao_domingo import render
elif modulo_nome == "agenda_manual":
    from src.pages.agenda_manual import render

render()
