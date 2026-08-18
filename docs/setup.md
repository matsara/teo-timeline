# Setup Local

## Pre-requisitos
| Item | Versao/Observacao |
|---|---|
| Python | 3.x |
| pip | Gerenciador de pacotes Python |
| SO | Linux, macOS ou Windows |

## Instalacao
1. Entrar na pasta do projeto.
2. (Opcional) criar e ativar ambiente virtual.
3. Instalar dependencias.

```bash
cd /home/samuel-freitas/workstation/teo-timeline
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requeriments.txt
```

## Configuracao
No estado atual, nao existe arquivo `.env` obrigatorio e nao ha credenciais no fluxo local.

### Variaveis de ambiente
| Variavel | Obrigatoria | Valor padrao | Observacao |
|---|---|---|---|
| Nenhuma | Nao | - | Nao ha variaveis de aplicacao obrigatorias confirmadas |

`TODO: validar` se em outro ambiente sera necessario configurar porta via variavel em vez de argumento CLI.

## Preparar ambiente
- O banco SQLite (`teo.db`) e criado/atualizado automaticamente na inicializacao via `app/db.py`.
- Nao ha etapa de migracao manual no fluxo atual.

## Executar localmente
```bash
cd /home/samuel-freitas/workstation/teo-timeline
python -m streamlit run teo_app.py --server.port 8501
```

Acesso local esperado:
- http://localhost:8501
