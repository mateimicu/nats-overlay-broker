#!/bin/bash

if [ $# -lt 1 ]
then
cat << HELP

dockertags  --  list all tags for a Docker image on a remote registry.

EXAMPLE: 
    - list all tags for ubuntu:
       dockertags ubuntu

    - list all php tags containing apache:
       dockertags php apache

HELP
fi

image="$1"
tags=`wget -q https://registry.hub.docker.com/v1/repositories/${image}/tags -O -  | sed -e 's/[][]//g' -e 's/"//g' -e 's/ //g' | tr '}' '\n'  | awk -F: '{print $3}'`

if [ -n "$2" ]
then
    tags=` echo "${tags}" | grep "$2" `
fi

LAST_TAG="$(echo "${tags}" | tr " " "\n" | sort -ur | grep -v 'latest' | head -n 1)"
PREFIX="$(echo $LAST_TAG | cut -d. -f-2)"
SUFIX="$(echo $LAST_TAG | cut -d. -f3)"
declare -i NEW_SUFIX num
NEW_SUFIX=1
NEW_SUFIX+="$SUFIX"
NEW_TAG="${PREFIX}.${NEW_SUFIX}"

echo "${NEW_TAG}"
