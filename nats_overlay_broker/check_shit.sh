#!/usr/bin/env bash
docker service logs ebs-cluster_broker-overlay | grep '[{"name": "color", "op": "<=", "val": "rosu"}, {"name": "height", "op": ">=", "val": 1.4}]' | grep 'Applied to' | grep 'broker.filter-subjects.b5b6802d-597b-493c-9615-ba19cfc0fa9b'

