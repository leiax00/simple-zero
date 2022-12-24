# !/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request

from bean.response import Response
from service.service import NovelService

name = 'api'

api = Blueprint(name, __name__)

service = NovelService()


@api.route('/query_book_list')
def query_book_list():
    book_list = service.get_book_list()
    return jsonify(Response().with_ok(book_list))


@api.route('/query_book/<bid>')
def query_book_by_bid(bid):
    book = service.get_book_by_id(bid)
    return jsonify(Response().with_ok(book))


@api.route('/query_catalog/<bid>')
def query_catalog_by_bid(bid):
    catalog = service.get_catalog_by_bid(bid)
    return jsonify(Response().with_ok(catalog))


@api.route('/query_chapter/<bid>/<cid>')
def query_chapter_by_bid(bid, cid):
    chapter = service.get_chapter_by_cid(bid, cid)
    return jsonify(Response().with_ok(chapter))


@api.route("/parse/single", methods=['POST'])
def parse_item():
    pass
