#!/bin/sh
#
# crontab setting like:
# * * * * * cd /home/vliu/WeChatService/send-wechat && sh ./scan_websites.sh >/tmp/scan-articles.log

set -x
echo 'running ...' $PWD
limit='3m'

timeout $limit python src/scan_bbc_top_story.py outbox/contacts.json
./cleanup.sh
timeout $limit python src/scan_bbc_most_read.py outbox/save.json
./cleanup.sh

timeout $limit python src/scan_nytimes_morning_brief.py outbox/contacts.json
./cleanup.sh
timeout $limit python src/scan_nytimes_opinion.py outbox/contacts.json
./cleanup.sh
timeout $limit python src/scan_nytimes_top_story.py outbox/save.json
./cleanup.sh

timeout $limit python src/scan_reuters_top_story.py outbox/save.json
./cleanup.sh

timeout $limit python src/scan_dw_top_story.py outbox/save.json
./cleanup.sh
timeout $limit python src/scan_dw_most_read.py outbox/save.json
./cleanup.sh

timeout $limit python src/scan_ft_top_story.py outbox/save.json

# if there is crashed process, the pids will be saved in .pid
# here we do clean up to kill those processes
./cleanup.sh
