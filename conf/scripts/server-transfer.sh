#!/bin/bash

# Database migration script.

# Load the conda commands.
source ~/miniconda3/etc/profile.d/conda.sh

# Activate the conda environemnt.
conda activate engine

# Stop on errors.
set -uex

# Set the configuration module.
TRANSFER_SETTINGS_MODULE=myforum.transfer.settings

# The database dump from old myforum (postgres sql dump).
# rsync -avz www@myforums.org:~/data/myforum-database-2.3.0-hourly-00.sql.gz export/sql/
DATABASE_SQL=export/sql/myforum-database-2.3.0-hourly-00.sql.gz

# The database the old dump is loaded from.
TRANSFER_DATABASE=transfer.db

# How many posts to load
LIMIT=1000

# Drop the old database if exists.
#dropdb --if-exists ${TRANSFER_DATABASE}

# Create the database for the old myforum.
#createdb ${TRANSFER_DATABASE}

# Load the data into the old myforum.
#cat ${DATABASE_SQL} | gunzip -c | psql -d ${TRANSFER_DATABASE}

# Transfer the data
python manage.py transfer --limit $LIMIT --settings ${TRANSFER_SETTINGS_MODULE}

