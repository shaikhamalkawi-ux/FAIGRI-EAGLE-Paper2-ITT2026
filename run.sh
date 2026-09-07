#!/usr/bin/env bash
set -euo pipefail
python reproduce.py
python verify_package.py
