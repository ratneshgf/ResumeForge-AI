#!/usr/bin/env bash
set -euo pipefail

# CPU-only PyTorch avoids downloading unused CUDA packages.
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements-render.txt
python -m spacy download en_core_web_md
python prepare_models.py
