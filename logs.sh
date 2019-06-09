#!/usr/bin/env bash
set -x
while true; do

	docker logs -f $(docker ps  | grep "$1" | awk '{print $1}')
	sleep 1
done
