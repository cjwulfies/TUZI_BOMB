#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname "$0")"
sudo apt-get update
sudo apt-get install -y python3-tk python3-venv python3-pil xauth
python3 -m venv .venv
. .venv/bin/activate
pip install -q --upgrade pip pyinstaller pillow
echo "deps ready"