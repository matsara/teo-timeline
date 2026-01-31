import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

# =========================================================
# 1. CONFIGURAÇÃO DA PÁGINA - IDENTIDADE TEO
# =========================================================
st.set_page_config(page_title="TEO - Timeline de Escalonamento", layout="wide")

st.markdown("""
    <style>
    [data-testid="stForm"] {border: none; padding: 0;}
    .stButton button {width: 100%;}
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. FUNÇÕES DE EXPORTAÇÃO HTML (RELATÓRIO ESTILIZADO)
# =========================================================
def gerar_html_final(alertas_selecionados):
    html_rows = ""
    for i, alerta in enumerate(alertas_selecionados):
        classe = "linha-clara" if i % 2 == 0 else "linha-escura"
        acionamentos = alerta["acionamentos"] if alerta["acionamentos"] else [{
            "nome": "-", "time": "-", "horario": "-", "atendeu": "-"
        }]

        primeira = acionamentos[0]
        restantes = acionamentos[1:]
        rowspan = len(acionamentos)

        html_rows += f"""
        <tr class="{classe}">
            <td rowspan="{rowspan}">{alerta['ticket']}</td>
            <td rowspan="{rowspan}">{alerta['evento']}</td>
            <td rowspan="{rowspan}">{alerta['status']}</td>
            <td>{primeira.get('nome', '-')}</td>
            <td>{primeira.get('time', '-')}</td>
            <td>{primeira.get('horario', '-')}</td>
            <td>{primeira.get('atendeu', '-')}</td>
        </tr>"""

        for a in restantes:
            html_rows += f"""
            <tr class="{classe}">
                <td>{a.get('nome', '-')}</td>
                <td>{a.get('time', '-')}</td>
                <td>{a.get('horario', '-')}</td>
                <td>{a.get('atendeu', '-')}</td>
            </tr>"""

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 0; padding: 0; }}
            th, td {{ border: 1px solid #000; padding: 8px; text-align: center; vertical-align: middle; font-size: 13px; }}
            th {{ background-color: #ff4d1a; color: white; font-weight: bold; }}
            .titulo {{ 
                background-color: #0b1f4d; color: white; font-size: 18px; 
                font-weight: bold; text-align: center; padding: 12px;
                border: 1px solid #000; border-bottom: none;
                margin-bottom: 0;
            }}
            .linha-clara {{ background-color: #ffffff; }}
            .linha-escura {{ background-color: #f7f7f7; }}
        </style>
    </head>
    <body>
        <div class="titulo">Timeline de Acionamentos</div>
        <table>
            <thead>
                <tr>
                    <th rowspan="2">Ticket</th>
                    <th rowspan="2">Evento</th>
                    <th rowspan="2">Status</th>
                    <th colspan="4">Acionamentos</th>
                </tr>
                <tr>
                    <th>Nome Completo</th>
                    <th>Time</th>
                    <th>Horário</th>
                    <th>Atendeu?</th>
                </tr>
            </thead>
            <tbody>{html_rows}</tbody>
        </table>
    </body>
    </html>
    """

# =========================================================
# 3. MODAL DE VISUALIZAÇÃO (POP-UP)
# =========================================================
@st.dialog("Visualização da Timeline TEO", width="large")
def modal_visualizacao(selecionados):
    html_content = gerar_html_final(selecionados)
    st.components.v1.html(html_content, height=450, scrolling=True)
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            label="💾 Baixar Arquivo HTML",
            data=html_content,
            file_name=f"teo_timeline_{datetime.now().strftime('%d-%m_%H%M')}.html",
            mime="text/html",
            type="primary"
        )
    with c2:
        if st.button("Fechar Visualização"):
            st.rerun()

# =========================================================
# 4. ESTADO GLOBAL E INTERFACE PRINCIPAL
# =========================================================
if "alertas" not in st.session_state:
    st.session_state.alertas = []
if "alerta_em_edicao" not in st.session_state:
    st.session_state.alerta_em_edicao = None

st.title("📊 TEO - Timeline de Escalonamento Organizado")

tab_geral, tab_novo = st.tabs(["📋 Painel de Alertas", "🟠 Registrar Novo Alerta"])

# --- TAB: CRIAR NOVO ALERTA ---
with tab_novo:
    st.header("Novo Alerta")
    with st.form("form_criar_alerta", clear_on_submit=True):
        col1, col2 = st.columns(2)
        ticket = col1.text_input("Número do Ticket")
        evento = col2.text_input("Nome do Evento")
        status = st.text_area("Status Atual")
        if st.form_submit_button("🚀 Criar Alerta"):
            if ticket and evento:
                st.session_state.alertas.append({
                    "id": str(uuid.uuid4()), "ticket": ticket, "evento": evento, 
                    "status": status, "acionamentos": []
                })
                st.success("Alerta criado com sucesso no TEO!")
                st.rerun()

# --- TAB: LISTAGEM E REPORT ---
with tab_geral:
    if not st.session_state.alertas:
        st.info("Nenhum alerta ativo no sistema.")
    else:
        selecionados = []
        h_check, h1, h2, h3, h4 = st.columns([0.5, 2, 3, 4, 1.5])
        h_check.caption("SEL.")
        h1.caption("TICKET")
        h2.caption("EVENTO")
        h3.caption("STATUS")
        h4.caption("AÇÕES")

        for alerta in list(st.session_state.alertas):
            with st.container(border=True):
                col_check, col1, col2, col3, col4 = st.columns([0.5, 2, 3, 4, 1.5])
                if col_check.checkbox("", key=f"check_{alerta['id']}"):
                    selecionados.append(alerta)
                col1.markdown(f"**{alerta['ticket']}**")
                col2.write(alerta["evento"])
                col3.write(alerta["status"])
                with col4:
                    c_edit, c_del = st.columns(2)
                    if c_edit.button("✏️", key=f"btn_edit_{alerta['id']}"):
                        st.session_state.alerta_em_edicao = alerta["id"]
                        st.rerun()
                    if c_del.button("🗑️", key=f"btn_del_{alerta['id']}"):
                        st.session_state.alertas.remove(alerta)
                        st.rerun()

        if selecionados:
            st.divider()
            st.subheader(f"📝 Report Consolidado ({len(selecionados)} itens)")
            
            resumo_txt = "📢 TEO - RESUMO DE ALERTAS\n" + "="*30 + "\n\n"
            for s in selecionados:
                resumo_txt += f"🎫 TICKET: {s['ticket']}\n🔥 EVENTO: {s['evento']}\n📌 STATUS: {s['status']}\n"
                if s['acionamentos']:
                    resumo_txt += "🕒 ESCALONAMENTO:\n"
                    for ac in s['acionamentos']:
                        resumo_txt += f"  - {ac['horario']} | {ac['nome']} ({ac['time']}) - Atendeu: {ac['atendeu']}\n"
                resumo_txt += "-"*20 + "\n\n"
            
            st.code(resumo_txt, language="text")

            if st.button("👁️ Visualizar e Gerar Timeline TEO", use_container_width=True):
                modal_visualizacao(selecionados)

# =========================================================
# 5. ÁREA DE GESTÃO (EDIÇÃO E ACIONAMENTOS)
# =========================================================
if st.session_state.alerta_em_edicao:
    st.divider()
    alerta_atual = next((a for a in st.session_state.alertas if a["id"] == st.session_state.alerta_em_edicao), None)
    
    if alerta_atual:
        st.header(f"⚙️ Gerenciar Ticket: {alerta_atual['ticket']}")
        col_ed_1, col_ed_2 = st.columns(2, gap="large")

        with col_ed_1:
            st.subheader("Dados do Evento")
            with st.form(key=f"form_ed_{alerta_atual['id']}"):
                alerta_atual["ticket"] = st.text_input("Ticket", alerta_atual["ticket"])
                alerta_atual["evento"] = st.text_input("Evento", alerta_atual["evento"])
                alerta_atual["status"] = st.text_area("Status", alerta_atual["status"])
                if st.form_submit_button("Atualizar Alerta"):
                    st.success("Dados salvos!")
                    st.rerun()

        with col_ed_2:
            st.subheader("Novo Escalonamento (Acionamento)")
            with st.form(key=f"form_ac_{alerta_atual['id']}", clear_on_submit=True):
                n = st.text_input("Nome Responsável")
                t = st.text_input("Time / Área")
                h_txt = st.text_input("Horário do Acionamento", value=datetime.now().strftime("%H:%M"))
                at = st.selectbox("Atendeu Chamado?", ["Sim", "Não", "-"])
                if st.form_submit_button("Adicionar à Timeline"):
                    if n and t:
                        alerta_atual["acionamentos"].append({
                            "nome": n, "time": t, "horario": h_txt, "atendeu": at
                        })
                        st.rerun()

        if alerta_atual["acionamentos"]:
            st.subheader("📋 Timeline do Escalonamento")
            for i, acion in enumerate(alerta_atual["acionamentos"]):
                c1, c2, c3, c4, c5 = st.columns([2, 1.5, 1, 1, 0.5])
                c1.write(f"👤 {acion['nome']}")
                c2.write(f"👥 {acion['time']}")
                c3.write(f"🕒 {acion['horario']}")
                c4.write(f"📞 {acion['atendeu']}")
                if c5.button("🗑️", key=f"del_acion_{alerta_atual['id']}_{i}"):
                    alerta_atual["acionamentos"].pop(i)
                    st.rerun()

        if st.button("⬅️ Sair do Gerenciamento"):
            st.session_state.alerta_em_edicao = None
            st.rerun()