# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import logging

from flask import Blueprint, jsonify, request, g, current_app

from config import xxl
from domain.response import Response
from utils.async_utils import async_run
from xxl_executor.config import XxlTask

name = 'xxl'

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
    task = XxlTask().fill_with_req(request.json)
    xxl.produce_task(task)
    return jsonify(Response().fill(200))


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
