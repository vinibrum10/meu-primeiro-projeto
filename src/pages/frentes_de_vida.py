import streamlit as st
from src.services.frente_service import (
    listar_frentes, criar_frente, atualizar_frente, obter_dividas_atencao
)

STATUS_OPTIONS = ["ativa", "pausada"]

EMOJI_DIVIDA = {
    "ok": "✅",
    "atenção": "⚠️",
    "crítico": "🔴",
    "pausada": "⏸️",
}


def render():
    st.title("🎯 Frentes de Vida")

    st.subheader("Nova frente")
    with st.form("nova_frente"):
        col1, col2 = st.columns([3, 1])
        with col1:
            nome = st.text_input("Nome da frente")
        with col2:
            limite = st.number_input("Limite (dias)", min_value=1, value=7)
        if st.form_submit_button("Adicionar"):
            if nome.strip():
                try:
                    criar_frente(nome, limite)
                    st.success(f"Frente '{nome}' criada!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro: {e}")
            else:
                st.error("Nome obrigatório.")

    st.divider()
    st.subheader("Frentes cadastradas")

    dividas = obter_dividas_atencao()
    if not dividas:
        st.info("Nenhuma frente cadastrada.")
        return

    for frente in dividas:
        divida = frente["divida"]
        emoji = EMOJI_DIVIDA.get(divida, "❓")
        ultima = frente.get("ultima_atividade")
        ultima_str = ultima[:10] if ultima else "nunca"

        with st.expander(f"{emoji} {frente['nome']} — {divida.upper()}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Status:** {frente['status']}")
                st.markdown(f"**Limite:** {frente['limite_dias']} dias")
                st.markdown(f"**Última atividade concluída:** {ultima_str}")
            with col2:
                with st.form(f"editar_frente_{frente['id']}"):
                    novo_nome = st.text_input("Nome", value=frente["nome"])
                    novo_limite = st.number_input(
                        "Limite (dias)", min_value=1, value=frente["limite_dias"]
                    )
                    novo_status = st.selectbox(
                        "Status",
                        STATUS_OPTIONS,
                        index=STATUS_OPTIONS.index(frente["status"]),
                    )
                    if st.form_submit_button("Salvar"):
                        atualizar_frente(frente["id"], novo_nome, novo_limite, novo_status)
                        st.success("Atualizado!")
                        st.rerun()
