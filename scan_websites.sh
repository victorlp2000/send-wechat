#!/bin/sh
#
# crontab setting like:
# * * * * * cd /home/vliu/WeChatService/send-wechat && sh ./scan_websites.sh >/tmp/scan-articles.log

set -x
echo 'running ...' $PWD
limit='3m'

timeout $limit python src/scan_article.py config/config_bbc-top-story.json
./cleanup.sh
timeout $limit python src/scan_article.py config/config_dw-top-story.json
./cleanup.sh
timeout $limit python src/scan_article.py config/config_nyt-morning-brief.json
./cleanup.sh

timeout $limit python src/scan_article.py config/config_nyt-opinion.json
./cleanup.sh
timeout $limit python src/scan_article.py config/config_nyt-top-story.json
./cleanup.sh
timeout $limit python src/scan_article.py config/config_reuters-top-story.json
./cleanup.sh
timeout $limit python src/scan_article.py config/config_bbc-most-read.json
./cleanup.sh
timeout $limit python src/scan_article.py config/config_dw-most-read.json
./cleanup.sh
timeout $limit python src/scan_article.py config/config_ft-top-story.json
./cleanup.sh
timeout $limit python src/scan_article.py config/config_voa-top-story.json
./cleanup.sh
timeout $limit python src/scan_article.py config/config_rfi-top-story.json
./cleanup.sh
timeout $limit python src/scan_article.py config/config_wsj-top-story.json
./cleanup.sh
