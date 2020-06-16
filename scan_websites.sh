#!/bin/sh
#
# crontab
# * * * * * /home/azure/WeChatService/send-wechat/scan_websites.sh >/tmp/scan_websites.log 2>&1
. $HOME/.profile
export DISPLAY=:0
cd $HOME/WeChatService/send-wechat
python src/scan_bbc_top_story.py outbox/contacts.json
python src/scan_nytimes_lead_news.py outbox/contacts.json
python src/scan_reuters_top_story.py outbox/contacts.json
