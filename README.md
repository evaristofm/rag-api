# rag-api

API de RAG (Retrieval-Augmented Generation) para perguntas e respostas sobre documentos de perfil, usando ChromaDB como vector store e Ollama para embeddings e geração de texto.

## Como funciona

1. Documentos de texto são enviados via `POST /v1/documents`, quebrados em chunks (por parágrafo) e indexados no ChromaDB, com embeddings gerados pelo Ollama.
2. Uma pergunta enviada via `GET /v1/ask` é usada para buscar os chunks mais relevantes no ChromaDB (opcionalmente filtrando por usuário) e montar um prompt de contexto, que é enviado a um LLM local via Ollama para gerar a resposta.

## Stack principal

| Lib | Uso |
| --- | --- |
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web / definição dos endpoints |
| [Pydantic](https://docs.pydantic.dev/) | Validação de request/response (`app/schemas`) |
| [ChromaDB](https://docs.trychroma.com/) | Vector store persistente para os chunks de documentos |
| [Ollama](https://ollama.com/) | Geração de embeddings (`nomic-embed-text`) e chat/LLM (`qwen2.5:0.5b`) |
| [uvicorn](https://www.uvicorn.org/) | Servidor ASGI |
| [Poetry](https://python-poetry.org/) | Gerenciamento de dependências e ambiente |
| [Ruff](https://docs.astral.sh/ruff/) | Lint e formatação |
| [pytest](https://docs.pytest.org/) + pytest-cov | Testes e cobertura |

Requer Python `>=3.14,<4.0`.

## Estrutura do projeto

```
app/
├── main.py                     # Cria o FastAPI app e inclui o router da v1
├── build_knowledge_base.py     # Script standalone: carrega profile.txt e popula o ChromaDB
├── core/
│   └── config.py               # Settings centralizadas (lidas de variáveis de ambiente)
├── services/
│   ├── vector_store.py         # VectorStoreService — encapsula o client ChromaDB (add/query)
│   └── llm.py                  # LLMService — encapsula a chamada de chat ao Ollama
├── api/
│   ├── deps.py                 # Providers dos services (FastAPI Depends + lru_cache)
│   └── v1/
│       └── routes/
│           ├── __init__.py     # Agrega os routers da v1
│           ├── document.py     # POST /documents
│           └── ask.py          # GET /ask
└── schemas/
    ├── document.py             # DocumentSubmission / DocumentResponse
    └── ask.py                  # AskResponse

tests/                          # Testes (pytest)
Dockerfile                      # Build da imagem da API
docker-compose.yml              # Sobe a API em container (conecta no Ollama do host)
```

## Variáveis de ambiente

Todas têm um valor padrão em `app/core/config.py`, então nenhuma é obrigatória para rodar localmente com Ollama na porta padrão.

| Variável | Padrão | Descrição |
| --- | --- | --- |
| `CHROMA_DB_PATH` | `./chroma_db` | Diretório onde o ChromaDB persiste os dados |
| `CHROMA_COLLECTION_NAME` | `personal_profile` | Nome da collection no ChromaDB |
| `EMBEDDING_MODEL` | `nomic-embed-text` | Modelo do Ollama usado para gerar embeddings |
| `OLLAMA_URL` | `http://localhost:11434` | URL do servidor Ollama |
| `LLM_MODEL` | `qwen2.5:0.5b` | Modelo do Ollama usado para responder as perguntas |

## Rodando localmente

Pré-requisitos: Python 3.14+, [Poetry](https://python-poetry.org/docs/#installation) e [Ollama](https://ollama.com/download) instalados.

```bash
# 1. Instalar as dependências (instala o Poetry se necessário)
./scripts/setup.sh

# 2. Baixar os modelos usados pela API
ollama pull nomic-embed-text
ollama pull qwen2.5:0.5b

# 3. Subir o servidor Ollama (se ainda não estiver rodando)
ollama serve

# 4. Subir a API em modo dev (reload automático)
poetry serve
# equivalente a: fastapi dev app/main.py
```

A API sobe em `http://localhost:8000` — docs interativas em `http://localhost:8000/docs`.

## Rodando com Docker Compose

O `docker-compose.yml` sobe só a API em container. O Ollama roda no host (fora do Docker) — o container acessa em `http://host.docker.internal:11434`.

```bash
# Pré-requisito: Ollama rodando no host com os modelos já baixados (ver seção acima)

docker compose up -d --build
```

A API fica disponível em `http://localhost:8000`. Os dados do ChromaDB são persistidos em `./chroma_db` (bind mount).

## Endpoints

### `POST /v1/documents`

Indexa um texto no ChromaDB, associado a um usuário.

```bash
curl -X POST http://localhost:8000/v1/documents \
  -H "Content-Type: application/json" \
  -d '{"user_name": "evaristo", "content": "Parágrafo 1.\n\nParágrafo 2."}'
```

### `GET /v1/ask`

Faz uma pergunta com base no contexto indexado. O parâmetro `user` é opcional e filtra a busca pelos documentos daquele usuário.

```bash
curl "http://localhost:8000/v1/ask?question=Qual+minha+profissao?&user=evaristo"
```

## Base de conhecimento inicial (opcional)

`app/build_knowledge_base.py` é um script standalone para popular o ChromaDB a partir de um arquivo `profile.txt` (não versionado) na raiz do projeto, com chunks separados por linha em branco.

```bash
poetry run python -m app.build_knowledge_base
```

## Comandos de desenvolvimento

Via [poethepoet](https://poethepoet.natn.io/) (tasks expostas direto como `poetry <task>`):

```bash
poetry lint     # ruff check
poetry format   # ruff check --fix + ruff format
poetry test     # lint + pytest + relatório de cobertura em html
```

## Pre-commit

O projeto usa [pre-commit](https://pre-commit.com/) para rodar automaticamente **black**, **isort**, **flake8**, **commitizen** e **pytest** antes de cada commit (config em `.pre-commit-config.yaml`).

```bash
# Instalar os hooks (pre-commit + commit-msg) — só precisa rodar uma vez
poetry run pre-commit install --install-hooks
```

A partir daí, todo `git commit` roda:
- `black` / `isort` / `flake8` — nos arquivos Python staged
- `pytest` — a suíte de testes completa (hook local, via `poetry run pytest`)
- `commitizen` — valida se a mensagem do commit segue o padrão [Conventional Commits](https://www.conventionalcommits.org/) (ex: `feat: ...`, `fix: ...`)

Para rodar os hooks manualmente sem commitar:

```bash
poetry run pre-commit run --all-files
```

> **Nota:** o projeto já usa [Ruff](https://docs.astral.sh/ruff/) para lint/format/isort (ver `poetry lint`/`poetry format` acima), configurado com aspas simples e 91 colunas. O `black` força aspas duplas (não é configurável), então rodar `black` via pre-commit vai reformatar aspas de forma diferente do `ruff format` — as duas ferramentas vão brigar entre si em cada commit/format. Ficou assim porque foi pedido explicitamente; se quiser eliminar esse atrito, a opção mais simples é remover `black`/`isort`/`flake8` do pre-commit e manter só o Ruff (que já cobre as três responsabilidades).

## Scripts

| Script | Uso |
| --- | --- |
| `scripts/setup.sh` | Instala o Poetry (se necessário) e o plugin `poetry-plugin-export`, instala as dependências do projeto (`poetry install`) e exporta `app/requirements.txt`, `app/requirements-dev.txt` e `app/requirements-test.txt` (sem hashes) |
| `scripts/update.sh` | Atualiza as dependências para as versões mais recentes permitidas (`poetry update`) e re-exporta os mesmos três arquivos de requirements |

Os grupos de dependências do Poetry (`dev` para lint/formatação, `test` para pytest) definem o conteúdo de `requirements-dev.txt` e `requirements-test.txt` — ver `[dependency-groups]` em `pyproject.toml`.
