#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname "$0")"
if [ -z "${DISPLAY:-}" ]; then
  echo "No DISPLAY. Use: ssh -C -Y user@host" >&2
  exit 1
fi
exec ./gifbomb "${@:-7}"