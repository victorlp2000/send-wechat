#!/bin/sh
#

pids=`cat .pid/*.pid`
echo kill -9 $pids
rm .pid/*.pid

