#!/bin/sh
#
# crontab
# * * * * * /home/azure/WeChatService/send-wechat/scan_websites.sh >/tmp/scan_websites.log 2>&1
#set -x

. $HOME/.profile
cd $HOME/WeChatService/send-wechat

python src/scan_bbc_top_story.py outbox/contacts.json
python src/scan_bbc_most_read.py outbox/contacts.json

python src/scan_nytimes_top_story.py outbox/contacts.json
python src/scan_nytimes_morning_brief.py outbox/contacts.json
python src/scan_nytimes_opinion.py outbox/contacts.json

python src/scan_reuters_top_story.py outbox/contacts.json

python src/scan_dw_most_read.py outbox/contacts.json

python src/scan_ft_top_story.py outbox/contacts.json