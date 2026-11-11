#!/usr/bin/env bash
# Claude Code Plugins Hub - Linux / macOS Setup
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if command -v python3 &>/dev/null; then
    python3 install.py
elif command -v python &>/dev/null; then
    python install.py
else
    echo "❌ Python 3 este necesar pentru instalare."
    exit 1
fi
