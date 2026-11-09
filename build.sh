#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname "$0")"
. .venv/bin/activate
pyinstaller --onefile --noconsole --clean --name gifbomb \
  --add-data "reaction.gif:." gifbomb.py
cp dist/gifbomb ./gifbomb
chmod +x ./gifbomb
echo "built: $(pwd)/gifbomb"