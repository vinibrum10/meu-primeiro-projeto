import streamlit as st
from src.services.semana_service import listar_semanas, obter_semana_atual
from src.services.financas_service import (
    obter_financas_semana, registrar_financas, metricas_financeiras, historico_financas
)


def render():
    st.title("💰 Finanças")

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

    registro = obter_financas_semana(semana_id)

    st.subheader("Registrar / atualizar finanças da semana")
    with st.form("financas_form"):
        col1, col2 = st.columns(2)
        with col1:
            gasto = st.number_input(
                "Gasto da semana (R$)",
                min_value=0.0,
                value=float(registro["gasto_semana"] if registro else 0),
                step=10.0,
                format="%.2f",
            )
        with col2:
            saldo = st.number_input(
                "Saldo atual (R$)",
                value=float(registro["saldo_atual"] if registro else 0),
                step=10.0,
                format="%.2f",
            )
        obs = st.text_area(
            "Observações",
            value=registro.get("observacoes") or "" if registro else "",
        )
        if st.form_submit_button("Salvar"):
            registrar_financas(semana_id, gasto, saldo, obs)
            st.success("Finanças registradas!")
            st.rerun()

    st.divider()
    st.subheader("Resumo financeiro")

    metricas = metricas_financeiras()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Gasto esta semana", f"R$ {metricas['gasto_semana_atual']:.2f}")
    with col2:
        saldo_val = metricas["saldo_atual"]
        st.metric("Saldo atual", f"R$ {saldo_val:.2f}")
    with col3:
        var = metricas["variacao_saldo"]
        if var is not None:
            delta_str = f"R$ {var:+.2f}"
            st.metric("Variação do saldo", delta_str, delta=delta_str)
        else:
            st.metric("Variação do saldo", "—")
    with col4:
        st.metric("Média semanal no mês", f"R$ {metricas['media_gasto_mensal']:.2f}")

    st.divider()
    st.subheader("Histórico")

    historico = historico_financas()
    if not historico:
        st.info("Nenhum registro financeiro ainda.")
        return

    for reg in historico:
        st.markdown(
            f"**{reg['data_inicio']} → {reg['data_fim']}** | "
            f"Gasto: R$ {reg['gasto_semana']:.2f} | "
            f"Saldo: R$ {reg['saldo_atual']:.2f}"
            + (f" | {reg['observacoes']}" if reg.get("observacoes") else "")
        )
