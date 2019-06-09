#!/usr/bin/env bash
while true; do
	docker logs -f $(docker ps  | grep "$1" | awk '{print $1}')
	echo "Retry ...."
	sleep 1
done
