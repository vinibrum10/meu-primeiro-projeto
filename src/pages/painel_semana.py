import streamlit as st
from src.services.semana_service import (
    obter_semana_atual, criar_semana_atual, atualizar_semana
)
from src.services.tarefa_service import progresso_semana
from src.services.frente_service import obter_dividas_atencao
from src.calculations import minutos_para_horas, data_inicio_semana_atual, data_fim_semana


EMOJI_DIVIDA = {
    "ok": "✅",
    "atenção": "⚠️",
    "crítico": "🔴",
    "pausada": "⏸️",
}

COR_DIVIDA = {
    "ok": "green",
    "atenção": "orange",
    "crítico": "red",
    "pausada": "gray",
}


def render():
    st.title("📋 Painel da Semana")

    inicio = data_inicio_semana_atual()
    fim = data_fim_semana(inicio)
    st.caption(f"Semana atual: {inicio.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}")

    semana = obter_semana_atual()

    if semana is None:
        st.info("Nenhuma semana cadastrada ainda. Clique abaixo para criar a semana atual.")
        with st.form("criar_semana"):
            foco = st.text_input("Foco principal da semana")
            tempo_livre = st.number_input("Tempo livre disponível (horas)", min_value=0.0, value=10.0, step=0.5)
            obs = st.text_area("Observações")
            if st.form_submit_button("Criar semana atual"):
                criar_semana_atual(foco, tempo_livre, obs)
                st.success("Semana criada!")
                st.rerun()
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Foco da semana")
        foco_atual = semana.get("foco_principal") or ""
        st.markdown(f"**{foco_atual}**" if foco_atual else "_Sem foco definido_")

        with st.expander("Editar semana"):
            with st.form("editar_semana"):
                foco = st.text_input("Foco principal", value=foco_atual)
                tempo_livre = st.number_input(
                    "Tempo livre (horas)", min_value=0.0,
                    value=float(semana.get("tempo_livre_horas") or 0), step=0.5
                )
                obs = st.text_area("Observações", value=semana.get("observacoes") or "")
                if st.form_submit_button("Salvar"):
                    atualizar_semana(semana["id"], foco, tempo_livre, obs)
                    st.success("Salvo!")
                    st.rerun()

    with col2:
        st.subheader("Progresso")
        prog = progresso_semana(semana["id"])
        st.metric("Tarefas", f"{prog['concluidas']}/{prog['total']}")
        st.metric("Concluído", f"{prog['percentual_concluido']}%")
        st.metric("Tempo realizado", minutos_para_horas(prog["tempo_realizado_min"]))

    st.divider()
    st.subheader("Dívida de atenção por frente")

    dividas = obter_dividas_atencao()
    if not dividas:
        st.info("Nenhuma frente cadastrada.")
        return

    criticas = [d for d in dividas if d["divida"] == "crítico"]
    atencao = [d for d in dividas if d["divida"] == "atenção"]
    ok = [d for d in dividas if d["divida"] == "ok"]
    pausadas = [d for d in dividas if d["divida"] == "pausada"]

    for grupo, titulo in [(criticas, "Crítico"), (atencao, "Atenção"), (ok, "Ok"), (pausadas, "Pausadas")]:
        if grupo:
            st.markdown(f"**{EMOJI_DIVIDA[grupo[0]['divida']]} {titulo}**")
            for d in grupo:
                ultima = d.get("ultima_atividade")
                ultima_str = ultima[:10] if ultima else "nunca"
                st.markdown(
                    f"- {d['nome']} — última atividade: {ultima_str} "
                    f"(limite: {d['limite_dias']} dias)"
                )
