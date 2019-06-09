#!/usr/bin/env bash

set -x
env
echo "Entry point"
touch /entrypoint_done
nats_overlay_broker "$MODE" --nats-server "$NATS_SERVERS" --redis-host "$REDIS_HOST" --redis-password "$REDIS_PASSWORD"
