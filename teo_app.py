from datetime import datetime

import streamlit as st

from app.db import init_db
from app.reports import (
    gerar_html_final,
    gerar_imagem_resumo_png,
    gerar_imagem_timeline_png,
    gerar_resumo_texto,
)
from app.services import (
    adicionar_acionamento,
    atualizar_alerta,
    criar_alerta,
    remover_acionamento,
    remover_alerta,
)
from app.sqlite_repository import SQLiteAlertasRepository


# =========================================================
# 1. CONFIGURACAO DA PAGINA
# =========================================================
st.set_page_config(page_title="TEO - Timeline de Escalonamento", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stForm"] {border: none; padding: 0;}
    .stButton button {width: 100%;}
    .stTabs [data-baseweb="tab-list"] {gap: 24px;}
    .stTabs [data-baseweb="tab"] {height: 50px; white-space: pre-wrap;}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 2. BANCO E REPOSITORIO
# =========================================================
init_db()
repo = SQLiteAlertasRepository()


@st.dialog("Visualizacao da Timeline TEO", width="large")
def modal_visualizacao(selecionados):
    html_content = gerar_html_final(selecionados)
    png_timeline_content = gerar_imagem_timeline_png(selecionados)
    png_resumo_content = gerar_imagem_resumo_png(selecionados)
    st.components.v1.html(html_content, height=450, scrolling=True)
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.download_button(
            label="Baixar Arquivo HTML",
            data=html_content,
            file_name=f"teo_timeline_{datetime.now().strftime('%d-%m_%H%M')}.html",
            mime="text/html",
            type="primary",
        )
    with c2:
        st.download_button(
            label="Baixar Timeline PNG",
            data=png_timeline_content,
            file_name=f"teo_timeline_{datetime.now().strftime('%d-%m_%H%M')}.png",
            mime="image/png",
        )
    with c3:
        st.download_button(
            label="Baixar Resumo PNG",
            data=png_resumo_content,
            file_name=f"teo_resumo_{datetime.now().strftime('%d-%m_%H%M')}.png",
            mime="image/png",
        )
    with c4:
        if st.button("Fechar Visualizacao"):
            st.rerun()


# =========================================================
# 3. ESTADO DE UI
# =========================================================
if "alerta_em_edicao" not in st.session_state:
    st.session_state.alerta_em_edicao = None


# =========================================================
# 4. INTERFACE PRINCIPAL
# =========================================================
st.title("TEO - Timeline de Escalonamento Organizado")

tab_geral, tab_todos, tab_novo = st.tabs(
    ["Painel de Alertas", "Todos os Alertas", "Registrar Novo Alerta"]
)


# --- TAB: CRIAR NOVO ALERTA ---
with tab_novo:
    st.header("Novo Alerta")
    with st.form(key="form_registro_alerta_principal", clear_on_submit=True):
        col1, col2 = st.columns(2)
        ticket_input = col1.text_input("Numero do Ticket")
        evento_input = col2.text_input("Nome do Evento")
        descricao_timeline_input = st.text_input(
            "Analista DOC",
            placeholder="Ex: Amado Batista",
        )

        if st.form_submit_button("Criar Alerta"):
            try:
                criar_alerta(
                    repo,
                    ticket_input,
                    evento_input,
                    descricao_timeline_input,
                )
                st.success("Alerta criado com sucesso!")
                st.rerun()
            except ValueError as erro:
                st.error(str(erro))


# --- TAB: LISTAGEM E REPORT ---
with tab_geral:
    alertas = repo.listar_alertas()

    if not alertas:
        st.info("Nenhum alerta ativo no sistema.")
    else:
        selecionados = []
        h_check, h1, h2, h3, h4, h5 = st.columns([0.5, 2, 3, 4, 1.3, 1.5])
        h_check.caption("SEL.")
        h1.caption("TICKET")
        h2.caption("EVENTO")
        h3.caption("STATUS ATUAL")
        h4.caption("REPORT")
        h5.caption("ACOES")

        for alerta in alertas:
            with st.container(border=True):
                col_check, col1, col2, col3, col4, col5 = st.columns([0.5, 2, 3, 4, 1.3, 1.5])

                if col_check.checkbox(
                    "Selecionar",
                    key=f"sel_{alerta['id']}",
                    label_visibility="collapsed",
                ):
                    selecionados.append(alerta)

                col1.markdown(f"**{alerta['ticket']}**")
                col2.write(alerta["evento"])
                col3.write(alerta.get("status_atual", "Sem acionamento"))

                with col4:
                    if st.button("Ver HTML", key=f"html_{alerta['id']}"):
                        modal_visualizacao([alerta])

                with col5:
                    c_edit, c_del = st.columns(2)
                    if c_edit.button("Editar", key=f"edit_{alerta['id']}"):
                        st.session_state.alerta_em_edicao = alerta["id"]
                        st.rerun()
                    if c_del.button("Excluir", key=f"del_{alerta['id']}"):
                        remover_alerta(repo, alerta["id"])
                        if st.session_state.alerta_em_edicao == alerta["id"]:
                            st.session_state.alerta_em_edicao = None
                        st.rerun()

        if selecionados:
            st.divider()
            st.subheader(f"Report Consolidado ({len(selecionados)} itens)")

            resumo_txt = gerar_resumo_texto(selecionados)

            st.code(resumo_txt, language="text")

            if st.button("Visualizar e Gerar Timeline TEO (HTML)", use_container_width=True):
                modal_visualizacao(selecionados)


with tab_todos:
    st.header("Todos os Alertas Criados")
    termo_ticket = st.text_input("🔎 Buscar por ticket", placeholder="Digite parte do ticket")

    alertas_todos = repo.buscar_alertas_por_ticket(termo_ticket)
    st.caption(f"{len(alertas_todos)} alerta(s) encontrado(s)")

    if not alertas_todos:
        st.info("Nenhum alerta encontrado para esse ticket.")
    else:
        for alerta in alertas_todos:
            titulo = f"{alerta['ticket']} | {alerta['evento']}"
            with st.expander(titulo, expanded=False):
                c1, c2, c3 = st.columns([2, 3, 2])
                c1.markdown(f"**Ticket:** {alerta['ticket']}")
                c2.markdown(f"**Evento:** {alerta['evento']}")
                c3.markdown(f"**Status Atual:** {alerta.get('status_atual', 'Sem acionamento')}")

                st.markdown(f"**Analista DOC:** {alerta.get('descricao_timeline') or '-'}")

                if alerta["acionamentos"]:
                    ultimo = alerta["acionamentos"][-1]
                    st.markdown(
                        "**Ultimo acionamento:** "
                        f"{ultimo['horario']} | {ultimo['nome']} ({ultimo['time']}) | "
                        f"Status: {ultimo.get('status_acionamento', '-')} | Atendeu: {ultimo['atendeu']}"
                    )
                else:
                    st.markdown("**Ultimo acionamento:** Sem acionamentos")

                if st.button("Visualizar e Gerar HTML", key=f"todos_html_{alerta['id']}"):
                    modal_visualizacao([alerta])


# =========================================================
# 5. AREA DE GESTAO (EDICAO E ACIONAMENTOS)
# =========================================================
if st.session_state.alerta_em_edicao:
    st.divider()
    alerta_atual = repo.buscar_alerta(st.session_state.alerta_em_edicao)

    if alerta_atual:
        st.header(f"Gerenciar Ticket: {alerta_atual['ticket']}")
        col_ed_1, col_ed_2 = st.columns(2, gap="large")

        with col_ed_1:
            st.subheader("Dados do Evento")
            with st.form(key=f"form_ed_dados_{alerta_atual['id']}"):
                ticket_edit = st.text_input("Ticket", alerta_atual["ticket"])
                evento_edit = st.text_input("Evento", alerta_atual["evento"])
                descricao_timeline_edit = st.text_input(
                    "Analista DOC",
                    alerta_atual.get("descricao_timeline") or "",
                )
                if st.form_submit_button("Atualizar Informacoes"):
                    try:
                        atualizar_alerta(
                            repo,
                            alerta_atual["id"],
                            ticket_edit,
                            evento_edit,
                            descricao_timeline_edit,
                        )
                        st.success("Dados atualizados!")
                        st.rerun()
                    except ValueError as erro:
                        st.warning(str(erro))

        with col_ed_2:
            st.subheader("Novo Acionamento (Escalonamento)")
            with st.form(key=f"form_novo_acionamento_{alerta_atual['id']}", clear_on_submit=True):
                nome = st.text_input("Analista acionado")
                time = st.text_input("Time / Area")
                horario_input = st.datetime_input("Data e hora do acionamento", value=datetime.now())
                status_acionamento = st.text_input(
                    "Status do acionamento",
                    placeholder="Ex: Acionado, em analise, aguardando retorno",
                )
                atendeu = st.selectbox("Atendeu Chamado?", ["Sim", "Nao", "-"])

                if st.form_submit_button("Adicionar a Timeline"):
                    try:
                        adicionar_acionamento(
                            repo,
                            alerta_atual["id"],
                            nome,
                            time,
                            horario_input.strftime("%d/%m/%Y %H:%M"),
                            atendeu,
                            status_acionamento,
                        )
                        st.rerun()
                    except ValueError as erro:
                        st.warning(str(erro))

        if alerta_atual["acionamentos"]:
            st.subheader("Timeline Atual deste Ticket")
            for acion in alerta_atual["acionamentos"]:
                with st.container(border=True):
                    c1, c2, c3, c4, c5, c6 = st.columns([2, 1.5, 1, 2, 1, 0.8])
                    c1.write(f"{acion['nome']}")
                    c2.write(f"{acion['time']}")
                    c3.write(f"{acion['horario']}")
                    c4.write(f"{acion.get('status_acionamento') or '-'}")
                    c5.write(f"{acion['atendeu']}")
                    if c6.button("Excluir", key=f"del_ac_{alerta_atual['id']}_{acion['id']}"):
                        remover_acionamento(repo, acion["id"])
                        st.rerun()

        if st.button("Sair da Edicao", type="secondary"):
            st.session_state.alerta_em_edicao = None
            st.rerun()
    else:
        st.session_state.alerta_em_edicao = None
        st.rerun()
