# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from flask import Blueprint, jsonify, request, g, current_app

from config import xxl
from domain.response import Response

name = 'xxl-executor'

api = Blueprint(name, __name__)


@api.route('/beat')
def heart_beat():
    return jsonify(Response().fill(200))


@api.route('/idleBeat', methods=['POST'])
def idle_beat():
    job_id = request.json.get('jobId')
    return jsonify(Response().fill(200))


@api.route('/run', methods=['POST'])
def run_task():
    params = {
        "job_id": request.json.get('jobId'),
        "job_name": request.json.get('executorHandler'),
        "job_params": request.json.get('executorParams'),
        "block_strategy": request.json.get('executorBlockStrategy'),
        "timeout": request.json.get('executorTimeout'),
        "log_id": request.json.get('logId'),
        "log_time": request.json.get('logDateTime'),
        "glue_type": request.json.get('glueType'),
        "glue_src": request.json.get('glueSource'),
        "glue_update_time": request.json.get('glueUpdatetime'),
        "broadcast_index": request.json.get('broadcastIndex'),
        "broadcast_total": request.json.get('broadcastTotal'),
    }

    rst = xxl.task_callback(**params)
    code = 200 if rst is not False else -1
    return jsonify(Response().fill(code, data=rst))


@api.route('/kill', methods=['POST'])
def kill_task():
    job_id = request.json.get('jobId')
    return jsonify(Response().fill(200))


@api.route('/log', methods=['POST'])
def get_log():
    log_id = request.json.get('logId')
    log_time = request.json.get('logDateTim')
    log_line_num = request.json.get('fromLineNum')
    logging.info(f'{log_id}, {log_time}, {log_line_num}')
    return jsonify(Response().fill(200))
