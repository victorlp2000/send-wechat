#!/usr/bin/python
# -*- coding: utf-8 -*-

import article

class ArticleNYTimes(article.Article):

    def disableSpecificElements(self):
        selectors = [
            "div.top_banner_ad",
            "div.setting-bar.row",
            "div.big_ad",
            "div.article-body-aside.col-lg-3",
            "div.container.article-footer",
            "nav.nav-footer.container",
            "div.download"
            ]
        ids = [
            "subscribe_cont",
            "subscribe_mobile_cont"
            ]
        article.Article.disableElements(self, selectors)
        article.Article.disableIds(self, ids)
