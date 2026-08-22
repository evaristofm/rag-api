#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

echo "Atualizando dependências do projeto..."
poetry update

echo "Exportando requirements para app/..."
poetry export -f requirements.txt --output app/requirements.txt --without-hashes
poetry export -f requirements.txt --output app/requirements-dev.txt --without-hashes --only dev
poetry export -f requirements.txt --output app/requirements-test.txt --without-hashes --only test

echo "Update concluído."
