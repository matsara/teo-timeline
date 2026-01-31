# 📊 TEO - Timeline de Escalonamento Organizado

O **TEO** é uma solução inteligente baseada em Python para a gestão de incidentes e monitoramento de escalonamentos em tempo real. Desenvolvido para facilitar o trabalho de equipes de Operações e Suporte, o TEO centraliza registros de tickets e automatiza a criação de timelines de acionamento.



## 🎯 Objetivo
Transformar o caos de múltiplos acionamentos em uma linha do tempo clara, auditável e fácil de compartilhar, garantindo que o status de cada escalonamento esteja sempre visível.

## 🚀 Funcionalidades Principais

- **Painel de Alertas:** Gestão centralizada de Tickets e Eventos críticos.
- **Escalonamento Detalhado:** Registro preciso de responsáveis, times, horários de acionamento e confirmação de atendimento.
- **Visualização Dinâmica:** Pop-up interno para conferência rápida da timeline antes da exportação.
- **Exportação Profissional:** Gerador de relatórios em HTML estilizado (tabelas listradas e organizadas) e resumo em texto para comunicadores (Slack/Teams).

## 🛠️ Especificações Técnicas

- **Frontend/Backend:** [Streamlit](https://streamlit.io/)
- **Processamento:** Pandas
- **Persistência Temporária:** Session State com identificadores UUID.
- **Relatórios:** Motor de renderização HTML5/CSS3 customizado.

## 📦 Instalação e Uso Local

1. Clone o repositório:
   ```bash
   git clone [https://github.com/seu-usuario/teo-app.git](https://github.com/seu-usuario/teo-app.git)