#!/usr/bin/python
# -*- coding: utf-8 -*-

import article

class ArticleBBC(article.Article):

    def disableSpecificElements(self):
        selectors = [
            'div.bbccom_slot.mpu-ad.bbccom_standard_slot.bbccom_visible',
            'ul.story-body__unordered-list',
            'div.share__back-to-top.ghost-column',
            'div.column--secondary',
            'div.navigation--footer',
        ]
        ids = [
            'bbccom_leaderboard_1_2_3_4',
            'bbccom_mpu_1_2',
            'core-navigation',
            'orb-aside'
        ]
        article.Article.disableElements(self, selectors)
        article.Article.disableIds(self, ids)
