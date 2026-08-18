# TEO - Documentacao Inicial

## Objetivo do projeto
O TEO e uma aplicacao Streamlit para registrar e acompanhar escalonamentos de incidentes, gerando uma timeline consolidada para comunicacao operacional.

## Visao geral
O fluxo principal permite:
- criar alertas (ticket, evento e Analista DOC);
- registrar acionamentos com data/hora, status do acionamento e atendimento;
- visualizar timeline em HTML;
- exportar HTML, resumo em texto e imagens PNG (timeline e resumo).

A persistencia oficial e feita em SQLite local (`teo.db`).

## Principais componentes
| Componente | Responsabilidade |
|---|---|
| `teo_app.py` | Interface Streamlit, fluxo de telas e acoes de usuario |
| `app/services.py` | Regras de negocio e validacoes basicas |
| `app/sqlite_repository.py` | Operacoes de leitura/escrita no banco SQLite |
| `app/db.py` | Conexao SQLite, schema e migracoes simples |
| `app/reports.py` | Geracao de HTML, resumo textual e imagens PNG |
| `app/repository.py` | Contrato de persistencia (Protocol) |

## Tecnologias
- Python 3
- Streamlit
- SQLite (`sqlite3` nativo)
- Pillow (PIL) para exportacao de imagem

## Fluxo resumido
1. Usuario cria um alerta.
2. Usuario adiciona acionamentos ao alerta.
3. Status atual do alerta e derivado do ultimo acionamento.
4. Usuario visualiza e exporta timeline em HTML/PNG.

## Leitura recomendada
- Arquitetura: [architecture.md](architecture.md)
- Setup local: [setup.md](setup.md)
- Operacao: [operations.md](operations.md)
- Deploy: [deployment.md](deployment.md)
