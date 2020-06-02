#!/usr/bin/python
# -*- coding: utf-8 -*-

import article

class ArticleBBC(article.Article):

    def disableSpecificElements(self):
        selectors = [
            'div.bbccom_slot.mpu-ad.bbccom_standard_slot.bbccom_visible',
            #'ul.story-body__unordered-list',
            'div.share__back-to-top.ghost-column',
            'div.column--secondary',
            'div.navigation--footer',
            'div.story-more',
            'div.tags-container',
            'div.share.share--lightweight.show.ghost-column'
        ]
        ids = [
            'bbccom_leaderboard_1_2_3_4',
            'bbccom_mpu_1_2',
            'core-navigation',
            'orb-aside',
            'comp-small-promo-group'
        ]
        article.Article.disableElements(self, selectors)
        article.Article.disableIds(self, ids)

        '''
        keep this kind <ul>
        <ul class="story-body__unordered-list">
          <li class="story-body__list-item">华为不能参与5G网络和千兆宽带网的核心网以及其他敏感设施的建设；</li>
        ...
        </ul>
        remove this kind <ul>
        <ul class="story-body__unordered-list">
          <li class="story-body__list-item"><a href="/zhongwen/simp/world-51297245" class="story-body__link">英国向华为5G开绿灯 引发国际反应和冲击波</a></li>
          ...
        </ul>
        '''
        unordered = 'ul.story-body__unordered-list'
        list = self.driver.find_elements_by_css_selector(unordered)
        for ul in list:
            a = ul.find_elements_by_tag_name('a')
            li = ul.find_elements_by_tag_name('li')
            if len(li) == len(a):
                self.driver.execute_script("arguments[0].style.display = 'none';", ul)
