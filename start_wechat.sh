# start python wechat will create .pid file in current folder
# where all pids will be saved inside. we need to kill them 
# after exit

rm *.pid

# start wechat
python src/wechat.py

# at exit, kill the pids and remove .pid file
pids=`cat *.pid`
kill -9 $pids
rm *.pid
