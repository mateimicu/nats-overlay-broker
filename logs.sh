#!/usr/bin/env bash
while true; do
	docker logs -f $(docker ps  | grep "$1" | awk '{print $1}') 2> /dev/null
	sleep 1
done
