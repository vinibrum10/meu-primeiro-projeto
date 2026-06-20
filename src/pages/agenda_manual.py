import streamlit as st
from src.services.semana_service import listar_semanas, obter_semana_atual
from src.services.agenda_service import listar_agenda, adicionar_item, excluir_item, DIAS_SEMANA


def render():
    st.title("📅 Agenda Manual")

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

    escolha = st.selectbox("Semana", chaves, index=idx_padrao)
    semana = opcoes_semana[escolha]
    semana_id = semana["id"]

    st.subheader("Adicionar item na agenda")
    with st.form("nova_agenda"):
        col1, col2, col3, col4 = st.columns([2, 1, 1, 3])
        with col1:
            dia = st.selectbox("Dia", DIAS_SEMANA)
        with col2:
            hora_inicio = st.text_input("Início", placeholder="08:00")
        with col3:
            hora_fim = st.text_input("Fim", placeholder="09:00")
        with col4:
            descricao = st.text_input("Descrição")
        if st.form_submit_button("Adicionar"):
            if descricao.strip():
                adicionar_item(semana_id, dia, hora_inicio, hora_fim, descricao)
                st.success("Adicionado!")
                st.rerun()
            else:
                st.error("Descrição obrigatória.")

    st.divider()
    st.subheader("Agenda da semana")

    agenda = listar_agenda(semana_id)
    if not agenda:
        st.info("Nenhum item na agenda desta semana.")
        return

    for dia in DIAS_SEMANA:
        itens_dia = [a for a in agenda if a["dia_semana"] == dia]
        if itens_dia:
            st.markdown(f"**{dia}**")
            for item in itens_dia:
                hora_str = ""
                if item.get("hora_inicio"):
                    hora_str = f"{item['hora_inicio']}"
                    if item.get("hora_fim"):
                        hora_str += f" → {item['hora_fim']}"
                    hora_str = f"`{hora_str}` "

                col1, col2 = st.columns([8, 1])
                with col1:
                    st.markdown(f"- {hora_str}{item['descricao']}")
                with col2:
                    if st.button("🗑️", key=f"del_agenda_{item['id']}", help="Remover"):
                        excluir_item(item["id"])
                        st.rerun()
            st.markdown("")
