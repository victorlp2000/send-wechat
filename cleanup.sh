#!/bin/sh
#

pids=`cat .pid/*.pid`
if [ ! -z "$pids" ]; then
  kill -9 $pids
  rm .pid/*.pid
fi
