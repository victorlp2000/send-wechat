#!/bin/sh
#
export DISPLAY=:1.0
cd $HOME/WeChatService/send-wechat
python src/scan_reuters_the_wire.py contacts.json >>wechat-reuters.log 2>&1
python src/scan_nytimes_morning-brief.py contacts.json >>wechat-nytimes.log 2>&1
python src/scan_nytimes_opinion.py contacts.json >>wechat-nytimes-opinion.log 2>&1
python src/scan_bbc_most_read.py contacts.json >>wechat-nytimes-opinion.log 2>&1


