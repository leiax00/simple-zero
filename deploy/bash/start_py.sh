#!/bin/bash

python -m venv sz
# 启动虚拟环境
. sz/bin/activate
python -m pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pip install -r requirement.txt \
            -i https://pypi.tuna.tsinghua.edu.cn/simple  \
            --trusted-host pypi.tuna.tsinghua.edu.cn

python app.py
