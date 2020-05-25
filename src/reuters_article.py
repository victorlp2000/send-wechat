#!/usr/bin/python
# -*- coding: utf-8 -*-

import article

class ArticleReuters(article.Article):

    def disableSpecificElements(self):
        selectors = [
            'div.Sticky_track.Leaderboard_sticky-container',
            'div.StandardArticleBody_dianomi-container.dianomi_context',
            'div.RelatedCoverage_related-coverage-module.module.RelatedCoverage_recirc',
            'div.DPSlot_container.StandardArticleBody_dp-slot-inline.StandardArticleBody_inline-canvas',
            'div.DPSlot_container',
            'div.TrendingStories_container',
            'div.footer-container',
            'div.Footer_links',
            'div.Footer_social',
            'div.StandardArticleBody_dp-slot-inline'
            ]
        article.Article.disableElements(self, selectors)
