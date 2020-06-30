#!/bin/sh
#
# crontab
# * * * * * cd /home/azure/WeChatService/send-wechat; sh ./scan_websites.sh >/tmp/scan_websites.log 2>&1
set -x
echo 'running ...' $PWD
limit='3m'
timeout $limit python src/scan_bbc_top_story.py outbox/contacts.json
timeout $limit python src/scan_bbc_most_read.py outbox/save.json

timeout $limit python src/scan_nytimes_top_story.py outbox/save.json
timeout $limit python src/scan_nytimes_morning_brief.py outbox/contacts.json
timeout $limit python src/scan_nytimes_opinion.py outbox/contacts.json

timeout $limit python src/scan_reuters_top_story.py outbox/contacts.json

timeout $limit python src/scan_dw_top_story.py outbox/contacts.json
timeout $limit python src/scan_dw_most_read.py outbox/save.json

timeout $limit python src/scan_ft_top_story.py outbox/contacts.json

# if there is crashed process, the pids will be saved in .pid
# here we do clean up to kill those processes
./cleanup.sh
