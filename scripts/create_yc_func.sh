#!/bin/bash

zip gh ./gh_parser.py scripts/requirements.txt -j

source .env

/opt/yc/bin/yc serverless function create --name=gh-parser

/opt/yc/bin/yc serverless function version create --function-name=gh-parser \
  --runtime python312 \
  --entrypoint gh_parser.handler \
  --memory 128m \
  --execution-timeout 600s \
  --source-path ./gh.zip \
  --environment GH_TOKEN=$GH_TOKEN,DB_USER=$DB_USER,DB_PASSWORD=$DB_PASSWORD,DB_PORT=$DB_PORT,DB_NAME=$DB_NAME,DB_HOSTNAME=$DB_HOSTNAME

rm gh.zip
