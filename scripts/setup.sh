#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

if ! command -v poetry &> /dev/null; then
  echo "Poetry não encontrado. Instalando..."
  curl -sSL https://install.python-poetry.org | python3 -
fi

if ! poetry self show plugins | grep -q poetry-plugin-export; then
  echo "Instalando poetry-plugin-export..."
  poetry self add poetry-plugin-export
fi

echo "Instalando dependências do projeto..."
poetry install

echo "Exportando requirements para app/..."
poetry export -f requirements.txt --output app/requirements.txt --without-hashes --without-urls
poetry export --with dev -f requirements.txt --output app/requirements-dev.txt --without-hashes --without-urls
poetry export --with test -f requirements.txt --output app/requirements-test.txt --without-hashes --without-urls

echo "Setup concluído."
