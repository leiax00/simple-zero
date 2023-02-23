# !/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify

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
