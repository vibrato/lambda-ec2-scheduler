#!/bin/bash
BASEDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pip install pytz -t "$BASEDIR"
zip -qr9 dist.zip lambda_function.py pytz*
ls -la dist.zip
