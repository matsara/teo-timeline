# Deploy

## Estado atual
Nao ha pipeline formal de deploy versionada no repositorio (CI/CD, Dockerfile, manifestos ou scripts dedicados).

## Processo disponivel hoje
O processo atual e execucao direta do Streamlit em ambiente local/host.

## Pre-requisitos
- Python 3
- Dependencias instaladas via `requeriments.txt`
- Acesso ao host onde o processo sera iniciado

## Build
Nao existe etapa de build dedicada no estado atual.

## Deploy / inicializacao
```bash
cd /home/samuel-freitas/workstation/teo-timeline
python -m pip install -r requeriments.txt
python -m streamlit run teo_app.py --server.port 8501
```

## Validacao pos-inicializacao
- Abrir `http://localhost:8501`.
- Criar um alerta de teste.
- Adicionar ao menos um acionamento.
- Validar exportacao HTML e PNG.

## Rollback
Nao existe procedimento formal de rollback documentado no projeto.

`TODO: validar` estrategia de versionamento e rollback quando houver ambiente de deploy formal.
