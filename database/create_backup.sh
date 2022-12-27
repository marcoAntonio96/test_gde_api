#!/bin/bash
cd backups
for variable in "$@"
do
    python create_backup.py "$variable"
done