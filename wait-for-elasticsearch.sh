#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

until curl -s -f "http://$host:9200" > /dev/null; do
  >&2 echo "Elasticsearch is unavailable - sleeping"
  sleep 5
done

until curl -s -f "http://$host:9200/_cluster/health?wait_for_status=yellow" > /dev/null; do
  >&2 echo "Elasticsearch is starting - waiting"
  sleep 5
done

>&2 echo "Elasticsearch is up - executing command"
exec $cmd