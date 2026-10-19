#!/usr/bin/env bash
cd "$(dirname "$0")"
./.venv/bin/python flower.py "$@"
