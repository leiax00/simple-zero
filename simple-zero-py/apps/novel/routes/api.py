# !/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify

from domain.response import Response
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
