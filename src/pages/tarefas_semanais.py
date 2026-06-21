import streamlit as st
from src.services.semana_service import listar_semanas, obter_semana_atual
from src.services.tarefa_service import (
    listar_tarefas_semana, criar_tarefa, atualizar_status_tarefa, excluir_tarefa
)
from src.services.frente_service import listar_frentes
from src.calculations import minutos_para_horas


STATUS_LABEL = {
    "pendente": "⬜ Pendente",
    "concluida": "✅ Concluída",
    "cancelada": "❌ Cancelada",
}

STATUS_OPTIONS = ["pendente", "concluida", "cancelada"]


def render():
    st.title("✅ Tarefas Semanais")

    semanas = listar_semanas()
    if not semanas:
        st.warning("Nenhuma semana cadastrada. Acesse o Painel da Semana para criar.")
        return

    opcoes_semana = {f"{s['data_inicio']} → {s['data_fim']}": s for s in semanas}
    semana_atual = obter_semana_atual()
    idx_padrao = 0
    chaves = list(opcoes_semana.keys())
    if semana_atual:
        chave_atual = f"{semana_atual['data_inicio']} → {semana_atual['data_fim']}"
        if chave_atual in chaves:
            idx_padrao = chaves.index(chave_atual)

    escolha = st.selectbox("Selecione a semana", chaves, index=idx_padrao)
    semana = opcoes_semana[escolha]
    semana_id = semana["id"]

    frentes = listar_frentes(apenas_ativas=True)
    if not frentes:
        st.warning("Nenhuma frente cadastrada.")
        return

    st.subheader("Adicionar tarefa")
    with st.form("nova_tarefa"):
        col1, col2 = st.columns([3, 1])
        with col1:
            descricao = st.text_input("Descrição da tarefa")
            frente_opcoes = {f["nome"]: f["id"] for f in frentes}
            frente_nome = st.selectbox("Frente de vida", list(frente_opcoes.keys()))
        with col2:
            tempo_plan = st.number_input("Tempo planejado (min)", min_value=0, value=0, step=15)
        if st.form_submit_button("Adicionar"):
            if descricao.strip():
                criar_tarefa(semana_id, frente_opcoes[frente_nome], descricao, tempo_plan)
                st.success("Tarefa adicionada!")
                st.rerun()
            else:
                st.error("Descrição obrigatória.")

    st.divider()
    st.subheader("Tarefas da semana")

    tarefas = listar_tarefas_semana(semana_id)
    if not tarefas:
        st.info("Nenhuma tarefa cadastrada para esta semana.")
        return

    frentes_usadas = sorted(set(t["frente_nome"] for t in tarefas))
    for frente_nome in frentes_usadas:
        tarefas_frente = [t for t in tarefas if t["frente_nome"] == frente_nome]
        with st.expander(f"**{frente_nome}** ({len(tarefas_frente)} tarefa(s))", expanded=True):
            for tarefa in tarefas_frente:
                col1, col2, col3, col4 = st.columns([4, 2, 2, 1])
                with col1:
                    st.markdown(f"{STATUS_LABEL[tarefa['status']]} {tarefa['descricao']}")
                with col2:
                    novo_status = st.selectbox(
                        "Status",
                        STATUS_OPTIONS,
                        index=STATUS_OPTIONS.index(tarefa["status"]),
                        key=f"status_{tarefa['id']}",
                        label_visibility="collapsed",
                    )
                with col3:
                    tempo_real = st.number_input(
                        "Realizado (min)",
                        min_value=0,
                        value=int(tarefa.get("tempo_realizado_min") or 0),
                        step=15,
                        key=f"tempo_{tarefa['id']}",
                        label_visibility="collapsed",
                    )
                with col4:
                    if st.button("💾", key=f"salvar_{tarefa['id']}", help="Salvar"):
                        atualizar_status_tarefa(tarefa["id"], novo_status, tempo_real)
                        st.rerun()

                if tarefa.get("tempo_planejado_min"):
                    st.caption(
                        f"Planejado: {minutos_para_horas(tarefa['tempo_planejado_min'])} | "
                        f"Realizado: {minutos_para_horas(tarefa.get('tempo_realizado_min') or 0)}"
                    )

                col_del1, col_del2 = st.columns([8, 1])
                with col_del2:
                    if st.button("🗑️", key=f"del_{tarefa['id']}", help="Excluir tarefa"):
                        excluir_tarefa(tarefa["id"])
                        st.rerun()
