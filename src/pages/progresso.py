import streamlit as st
from src.services.semana_service import listar_semanas
from src.services.tarefa_service import progresso_semana, listar_tarefas_semana
from src.calculations import minutos_para_horas


def render():
    st.title("📈 Progresso")

    semanas = listar_semanas()
    if not semanas:
        st.warning("Nenhuma semana cadastrada.")
        return

    opcoes_semana = {f"{s['data_inicio']} → {s['data_fim']}": s for s in semanas}
    escolha = st.selectbox("Selecione a semana", list(opcoes_semana.keys()))
    semana = opcoes_semana[escolha]
    semana_id = semana["id"]

    prog = progresso_semana(semana_id)

    st.subheader("Resumo da semana")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de tarefas", prog["total"])
    with col2:
        st.metric("Concluídas", prog["concluidas"])
    with col3:
        st.metric("% Concluído", f"{prog['percentual_concluido']}%")
    with col4:
        st.metric("Frentes ativas", prog["frentes_com_acao"])

    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("Tempo planejado", minutos_para_horas(prog["tempo_planejado_min"]))
    with col6:
        st.metric("Tempo realizado", minutos_para_horas(prog["tempo_realizado_min"]))
    with col7:
        st.metric("Pendentes", prog["pendentes"])

    if prog["total"] > 0:
        st.progress(prog["percentual_concluido"] / 100)

    st.divider()
    st.subheader("Por frente de vida")

    tarefas = listar_tarefas_semana(semana_id)
    if not tarefas:
        st.info("Nenhuma tarefa cadastrada.")
        return

    frentes_usadas = sorted(set(t["frente_nome"] for t in tarefas))
    for frente_nome in frentes_usadas:
        tarefas_frente = [t for t in tarefas if t["frente_nome"] == frente_nome]
        total = len(tarefas_frente)
        concluidas = sum(1 for t in tarefas_frente if t["status"] == "concluida")
        pct = round(concluidas / total * 100) if total > 0 else 0

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{frente_nome}** — {concluidas}/{total} ({pct}%)")
            st.progress(pct / 100)
        with col2:
            tempo_plan = sum(t.get("tempo_planejado_min", 0) or 0 for t in tarefas_frente)
            tempo_real = sum(t.get("tempo_realizado_min", 0) or 0 for t in tarefas_frente)
            st.caption(f"Plan: {minutos_para_horas(tempo_plan)}")
            st.caption(f"Real: {minutos_para_horas(tempo_real)}")

    st.divider()
    st.subheader("Visão geral — todas as semanas")

    dados_historicos = []
    for semana_hist in semanas:
        p = progresso_semana(semana_hist["id"])
        if p["total"] > 0:
            dados_historicos.append({
                "Semana": semana_hist["data_inicio"],
                "Total": p["total"],
                "Concluídas": p["concluidas"],
                "% Concluído": p["percentual_concluido"],
            })

    if dados_historicos:
        import pandas as pd
        df = pd.DataFrame(dados_historicos)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum dado histórico disponível.")
