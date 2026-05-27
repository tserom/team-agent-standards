#!/usr/bin/env bash
# 按 Agent 分别构建：./scripts/build.sh <agent-id>  或  ./scripts/build.sh --list
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${SCRIPT_DIR}/build.py" "$@"
