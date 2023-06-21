# !/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request

from domain.response import Response
from service.j2wx_serve import j2wx_serve
from service.service import novel

name = 'api'

api = Blueprint(name, __name__)

service = novel


@api.route('/book/<bid>')
def query_book_by_bid(bid):
    book = service.get_book_by_id(bid)
    return jsonify(Response().with_ok(book))


@api.route('/search/<book_name>')
def query_book_by_name(book_name):
    book = service.get_book_by_name(book_name)
    return jsonify(Response().with_ok(book))


@api.route('/chapter/<bid>/<cid>')
def query_book_chapter(bid, cid):
    chapter = service.get_chapter(bid, cid)
    return jsonify(Response().with_ok(chapter))


@api.route('/bookshelf', defaults={'group_name': 'default'})
@api.route('/bookshelf/<group_name>')
def get_book_list(group_name):
    book_list = service.get_book_list(group_name)
    return jsonify(Response().with_ok(book_list))


@api.route('/book/subscribe/<bid>', defaults={'cid': None})
@api.route('/book/subscribe/<bid>/<cid>')
def subscribe_book(bid, cid):
    """
    收藏书籍, 如果传入了cid则表示在章节页面收藏, 否则为简介页面收藏
    :param bid: 书籍id
    :param cid: 章节id
    :return: 收藏结果
    """
    ok = service.subscribe_book(bid, cid)
    return jsonify(Response.with_ok(ok))


@api.route('/j2wx/channel/<channel_key>')
def get_rank_list(channel_key):
    """
    获取分频下的榜单列表
    :param channel_key: 分频
    :return: 榜单列表
    """
    return jsonify(Response().with_ok(j2wx_serve.get_rank_list(channel_key)))


@api.route('/j2wx/channel/<channel_key>/<rank_id>')
def get_rank_info(channel_key, rank_id):
    """
    获取榜单的数据信息
    :param channel_key: 分频
    :param rank_id: 榜单id
    :return: 榜单数据
    """
    return jsonify(Response().with_ok(j2wx_serve.get_rank_info(channel_key, rank_id)))


@api.route('/j2wx/custom-rank/<rank_id>')
def get_custom_rank_info(rank_id):
    """
    获取自定义榜单的书籍信息
    :param rank_id: 自定义榜单的id
    :return: 榜单数据
    """
    before_hour = request.args.get('beforeHour', 7 * 24)
    return jsonify(Response().with_ok(j2wx_serve.get_custom_rank_info(rank_id, int(before_hour))))


@api.route('/j2wx/custom-rank/new', methods=['POST'])
def save_custom_rank():
    """
    保存自定义榜单
    :return: 自定义榜单
    """
    data = request.json
    try:
        return jsonify(Response().with_ok(j2wx_serve.save_custom_rank(data)))
    except Exception as e:
        return jsonify(Response().fill(-1, e.__str__()))


@api.route('/j2wx/custom-rank/load')
def get_custom_rank_by_key():
    """
    通过秘钥获取自定义榜单
    :return:
    """
    key = request.args.get('key')
    rank = j2wx_serve.get_custom_rank_by_key(key)
    if rank is None:
        return jsonify(Response().fill(-1, 'NO_RANK'))
    return jsonify(Response().with_ok(rank))


@api.route('/j2wx/custom-rank/del', methods=['DELETE'])
def del_custom_rank():
    """
    删除自定义榜单
    :return:
    """
    data = request.args.get('ids', '').split(',')
    return jsonify(Response().with_ok(j2wx_serve.del_custom_rank(data)))


@api.route('/j2wx/custom-rank/add-novel', methods=['PUT'])
def add_novel_2_custom_rank():
    """
    添加书籍到自定义榜单中
    :return: 添加结果
    """
    data = request.json
    rank_id = data.get('rankId')
    novel_ids = data.get('ids')
    if rank_id is None or novel_ids is None:
        return jsonify(Response().fill(-1, 'PARAM_ERR'))

    if isinstance(novel_ids, str):
        novel_ids = [novel_ids]

    return jsonify(Response().with_ok(j2wx_serve.add_novel_2_custom_rank(rank_id, novel_ids)))


@api.route('/j2wx/custom-rank/del-novel', methods=['DELETE'])
def remove_novel_from_custom_rank():
    """
    从自定义榜单中移除小说
    :return:
    """
    rank_id = request.args.get('rankId')
    novel_ids = request.args.get('ids').split(',')
    if rank_id is None or novel_ids is None:
        return jsonify(Response().fill(-1, 'PARAM_ERR'))

    return jsonify(Response().with_ok(j2wx_serve.remove_novel_from_custom_rank(rank_id, novel_ids)))
