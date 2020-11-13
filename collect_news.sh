#!/bin/sh
#
# crontab setting like:
# 10 0 * * * cd /home/vliu/WeChatService/send-wechat && sh ./collect_news.sh >/tmp/collect_news.log

set -x
echo 'running ...' $PWD
limit='3m'

timeout $limit python src/collect.py config/config_collect.json
