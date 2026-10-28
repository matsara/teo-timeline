# Operacoes Atuais

## Iniciar aplicacao
```bash
cd /home/samuel-freitas/workstation/teo-timeline
python -m streamlit run teo_app.py --server.port 8501
```

## Parar aplicacao
No terminal onde o Streamlit esta em execucao:
- `Ctrl + C`

## Processos manuais principais
| Processo | Como executar |
|---|---|
| Criar alerta | Aba "Registrar Novo Alerta" |
| Editar alerta | Botao "Editar" no painel |
| Adicionar acionamento | Area "Novo Acionamento" dentro da gestao do ticket |
| Gerar HTML | Botao "Ver HTML" ou "Visualizar e Gerar Timeline TEO (HTML)" |
| Exportar PNG | No dialog de visualizacao, botoes de download PNG |

## Verificar status
- Aplicacao ativa quando a URL local responde: `http://localhost:8501`.
- Logs aparecem no terminal que iniciou o Streamlit.

## Consultar logs
- O log operacional atual e o stdout/stderr do processo Streamlit.
- Nao existe rotacao de logs configurada no projeto.

## Troubleshooting basico
| Sintoma | Acao recomendada |
|---|---|
| Porta 8501 em uso | Subir em outra porta: `--server.port 8502` |
| Erro de dependencia | Reinstalar com `python -m pip install -r requeriments.txt` |
| Comportamento antigo na UI | Reiniciar processo Streamlit |
| Erro no banco local | Encerrar app e validar arquivo `teo.db` |
