#!/usr/bin/env bash
while true; do
	mkdir -p container-logs
	LOG_DATE=$(date '+%Y-%m-%d-%H:%M:%S')
	docker logs -f $(docker ps  | grep "$1" | awk '{print $1}') | tee -a "container-logs/$1-$LOG_DATE"
	echo "Retry ...."
	sleep 1
done
