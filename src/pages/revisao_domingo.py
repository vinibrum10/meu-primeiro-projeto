import streamlit as st
from src.services.semana_service import listar_semanas, obter_semana_atual
from src.services.revisao_service import obter_revisao, salvar_revisao
from src.services.tarefa_service import progresso_semana
from src.calculations import minutos_para_horas


def render():
    st.title("🌙 Revisão de Domingo")

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

    escolha = st.selectbox("Semana para revisar", chaves, index=idx_padrao)
    semana = opcoes_semana[escolha]
    semana_id = semana["id"]

    prog = progresso_semana(semana_id)
    st.subheader("Resumo da semana")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tarefas", f"{prog['concluidas']}/{prog['total']}")
    with col2:
        st.metric("% Concluído", f"{prog['percentual_concluido']}%")
    with col3:
        st.metric("Tempo realizado", minutos_para_horas(prog["tempo_realizado_min"]))

    foco = semana.get("foco_principal") or "_sem foco definido_"
    st.markdown(f"**Foco da semana:** {foco}")

    st.divider()
    revisao = obter_revisao(semana_id)

    st.subheader("Reflexão semanal")
    with st.form("revisao_form"):
        bem = st.text_area(
            "O que foi bem?",
            value=revisao.get("o_que_foi_bem") or "" if revisao else "",
            height=100,
        )
        melhorar = st.text_area(
            "O que pode melhorar?",
            value=revisao.get("o_que_melhorar") or "" if revisao else "",
            height=100,
        )
        aprendizados = st.text_area(
            "Aprendizados",
            value=revisao.get("aprendizados") or "" if revisao else "",
            height=80,
        )
        nota = st.slider(
            "Nota da semana (1-10)",
            min_value=1,
            max_value=10,
            value=int(revisao.get("nota_semana") or 7) if revisao else 7,
        )
        if st.form_submit_button("Salvar revisão"):
            salvar_revisao(semana_id, bem, melhorar, aprendizados, nota)
            st.success("Revisão salva!")
            st.rerun()

    if revisao:
        st.caption(f"Última revisão: {revisao.get('revisado_em', '')[:16]}")
