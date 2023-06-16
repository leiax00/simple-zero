# !/usr/bin/env python
# -*- coding: utf-8 -*-
from data.bi_qu_ge.parser import BiQuHtmlParser
from utils.httpHelper import *

domain = 'https://www.biquzw.info/'


class APIS(Enum):
    # params={'searchkey': book_name}
    search = Api('/modules/article/search.php', HttpMethod.GET)
    # book_id=bid
    catalog = Api('/{book_id}/', HttpMethod.GET)
    # book_id=chapter.bid, chapter_id=chapter.cid
    chapter = Api('/{book_id}/{chapter_id}.html', HttpMethod.GET)


parser = BiQuHtmlParser()
