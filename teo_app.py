import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

# =========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(page_title="TEO - Timeline de Escalonamento", layout="wide")

# CSS para melhorar a estética e garantir que os botões ocupem o espaço
st.markdown("""
    <style>
    [data-testid="stForm"] {border: none; padding: 0;}
    .stButton button {width: 100%;}
    .stTabs [data-baseweb="tab-list"] {gap: 24px;}
    .stTabs [data-baseweb="tab"] {height: 50px; white-space: pre-wrap;}
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. FUNÇÕES DE SUPORTE
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
# 3. INICIALIZAÇÃO DO ESTADO (SESSION STATE)
# =========================================================
if "alertas" not in st.session_state:
    st.session_state.alertas = []
if "alerta_em_edicao" not in st.session_state:
    st.session_state.alerta_em_edicao = None

# =========================================================
# 4. INTERFACE PRINCIPAL
# =========================================================
st.title("📊 TEO - Timeline de Escalonamento Organizado")

tab_geral, tab_novo = st.tabs(["📋 Painel de Alertas", "🟠 Registrar Novo Alerta"])

# --- TAB: CRIAR NOVO ALERTA ---
with tab_novo:
    st.header("Novo Alerta")
    # KEY ÚNICA PARA O FORMULÁRIO DE CRIAÇÃO
    with st.form(key="form_registro_alerta_principal", clear_on_submit=True):
        col1, col2 = st.columns(2)
        ticket_input = col1.text_input("Número do Ticket")
        evento_input = col2.text_input("Nome do Evento")
        status_input = st.text_area("Status Atual / Descrição")
        
        if st.form_submit_button("🚀 Criar Alerta"):
            if ticket_input and evento_input:
                novo_alerta = {
                    "id": str(uuid.uuid4()), 
                    "ticket": ticket_input, 
                    "evento": evento_input, 
                    "status": status_input, 
                    "acionamentos": []
                }
                st.session_state.alertas.append(novo_alerta)
                st.success("Alerta criado com sucesso!")
                st.rerun()
            else:
                st.error("Preencha Ticket e Evento para continuar.")

# --- TAB: LISTAGEM E REPORT ---
with tab_geral:
    if not st.session_state.alertas:
        st.info("Nenhum alerta ativo no sistema.")
    else:
        selecionados = []
        # Cabeçalho da Tabela no Streamlit
        h_check, h1, h2, h3, h4 = st.columns([0.5, 2, 3, 4, 1.5])
        h_check.caption("SEL.")
        h1.caption("TICKET")
        h2.caption("EVENTO")
        h3.caption("STATUS")
        h4.caption("AÇÕES")

        for alerta in st.session_state.alertas:
            with st.container(border=True):
                col_check, col1, col2, col3, col4 = st.columns([0.5, 2, 3, 4, 1.5])
                
                # Checkbox para seleção no report
                if col_check.checkbox("", key=f"sel_{alerta['id']}"):
                    selecionados.append(alerta)
                
                col1.markdown(f"**{alerta['ticket']}**")
                col2.write(alerta["evento"])
                col3.write(alerta["status"])
                
                with col4:
                    c_edit, c_del = st.columns(2)
                    if c_edit.button("✏️", key=f"edit_{alerta['id']}"):
                        st.session_state.alerta_em_edicao = alerta["id"]
                        st.rerun()
                    if c_del.button("🗑️", key=f"del_{alerta['id']}"):
                        st.session_state.alertas.remove(alerta)
                        st.rerun()

        if selecionados:
            st.divider()
            st.subheader(f"📝 Report Consolidado ({len(selecionados)} itens)")
            
            # Gerador de texto rápido para copiar/colar
            resumo_txt = "📢 TEO - RESUMO DE ALERTAS\n" + "="*30 + "\n\n"
            for s in selecionados:
                resumo_txt += f"🎫 TICKET: {s['ticket']}\n🔥 EVENTO: {s['evento']}\n📌 STATUS: {s['status']}\n"
                if s['acionamentos']:
                    resumo_txt += "🕒 ESCALONAMENTO:\n"
                    for ac in s['acionamentos']:
                        resumo_txt += f"  - {ac['horario']} | {ac['nome']} ({ac['time']}) - Atendeu: {ac['atendeu']}\n"
                resumo_txt += "-"*20 + "\n\n"
            
            st.code(resumo_txt, language="text")

            if st.button("👁️ Visualizar e Gerar Timeline TEO (HTML)", use_container_width=True):
                modal_visualizacao(selecionados)

# =========================================================
# 5. ÁREA DE GESTÃO (EDIÇÃO E ACIONAMENTOS)
# =========================================================
if st.session_state.alerta_em_edicao:
    st.divider()
    # Busca o alerta atual pelo ID
    alerta_atual = next((a for a in st.session_state.alertas if a["id"] == st.session_state.alerta_em_edicao), None)
    
    if alerta_atual:
        st.header(f"⚙️ Gerenciar Ticket: {alerta_atual['ticket']}")
        col_ed_1, col_ed_2 = st.columns(2, gap="large")

        # Coluna 1: Edição dos dados básicos
        with col_ed_1:
            st.subheader("Dados do Evento")
            with st.form(key=f"form_ed_dados_{alerta_atual['id']}"):
                alerta_atual["ticket"] = st.text_input("Ticket", alerta_atual["ticket"])
                alerta_atual["evento"] = st.text_input("Evento", alerta_atual["evento"])
                alerta_atual["status"] = st.text_area("Status Atual", alerta_atual["status"])
                if st.form_submit_button("Atualizar Informações"):
                    st.success("Dados atualizados!")
                    st.rerun()

        # Coluna 2: Inserção de novos acionamentos
        with col_ed_2:
            st.subheader("Novo Acionamento (Escalonamento)")
            with st.form(key=f"form_novo_acionamento_{alerta_atual['id']}", clear_on_submit=True):
                n = st.text_input("Nome Responsável")
                t = st.text_input("Time / Área")
                h = st.text_input("Horário do Acionamento")

                at = st.selectbox("Atendeu Chamado?", ["Sim", "Não", "-"])
                
                if st.form_submit_button("Adicionar à Timeline"):
                    if n and t:
                        alerta_atual["acionamentos"].append({
                            "nome": n, 
                            "time": t, 
                            "horario": h,
                            "atendeu": at
                        })
                        st.rerun()
                    else:
                        st.warning("Preencha Nome e Time do responsável.")

        # Exibição da Timeline do Ticket Específico
        if alerta_atual["acionamentos"]:
            st.subheader("📋 Timeline Atual deste Ticket")
            for i, acion in enumerate(alerta_atual["acionamentos"]):
                with st.container(border=True):
                    c1, c2, c3, c4, c5 = st.columns([2, 1.5, 1, 1, 0.5])
                    c1.write(f"👤 {acion['nome']}")
                    c2.write(f"👥 {acion['time']}")
                    c3.write(f"🕒 {acion['horario']}")
                    c4.write(f"📞 {acion['atendeu']}")
                    if c5.button("🗑️", key=f"del_ac_{alerta_atual['id']}_{i}"):
                        alerta_atual["acionamentos"].pop(i)
                        st.rerun()

        st.write("")
        if st.button("⬅️ Sair da Edição", type="secondary"):
            st.session_state.alerta_em_edicao = None
            st.rerun()