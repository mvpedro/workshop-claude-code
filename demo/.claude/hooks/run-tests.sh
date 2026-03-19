#!/bin/bash
# Hook: Roda testes automaticamente após cada edição de arquivo
# Configurado em .claude/settings.json como PostToolUse hook
cd "$(git rev-parse --show-toplevel)/demo" || exit 0
python -m pytest tests/ --tb=line -q 2>&1 | tail -5
