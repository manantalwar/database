#!/usr/bin/env bash

aws s3 cp ./lrc_database/db.sqlite3 s3://lrc-database-backups/db-$(date -I).sqlite3
