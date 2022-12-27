#!/bin/bash
cd backups
for variable in "$@"
do
    python load_backup.py "$variable"
done