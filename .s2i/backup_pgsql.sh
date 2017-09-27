#!/bin/bash
# Backs up the OpenShift PostgreSQL database for this application
# by Skye Book <skye.book@gmail.com>

NOW="$(date +"%Y-%m-%d")"
FILENAME="/var/lib/pgsql/data/backups"
pg_dump -F t -U $PGUSER statnuts | gzip > $FILENAME