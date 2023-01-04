# !/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify

from domain.response import Response
from service.service import NovelService

name = 'api'

api = Blueprint(name, __name__)

service = NovelService()


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


@api.route('/book/list', defaults={'group_name': 'default'})
@api.route('/book/list/<group_name>')
def get_book_list(group_name):
    book_list = service.get_book_list(group_name)
    return jsonify(Response().with_ok(book_list))


@api.route('/book/subscribe/<bid>')
def subscribe_book(bid):
    ok = service.subscribe_book(bid)
    return jsonify(Response.with_ok(ok))
