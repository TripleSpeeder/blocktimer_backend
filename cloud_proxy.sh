#!/bin/bash
source .env
cloud_sql_proxy -instances="$DATABASE_INSTANCE"=tcp:3306
