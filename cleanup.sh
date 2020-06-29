#!/bin/sh
#

pids=`cat .pid/*.pid`
if [ ! -z "$pids" ]; then
  echo kill -9 $pids
  rm .pid/*.pid
fi
