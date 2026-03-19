#!/bin/bash
set -e
echo "Gerando documentação via Claude Code..."
claude -p "$(cat prompts/full-scan.md)" --allowedTools Edit,Write,Read,Glob,Grep,Bash
echo "Documentação gerada em docs/"
