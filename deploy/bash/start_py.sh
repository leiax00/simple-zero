#!/bin/bash

pwd
echo "$WORK_DIR"/.venv/bin/activate

python -m venv .venv
source "$WORK_DIR"/.venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirement.txt \
            -i https://pypi.tuna.tsinghua.edu.cn/simple  \
            --trusted-host pypi.tuna.tsinghua.edu.cn

python app.py
