#!/usr/bin/env bash

echo ''
echo 'activating virtual environment'
echo ''

python -m venv env
echo ''


source env/bin/activate
echo ''

echo ''
echo 'installing requirements'
echo ''

pip3 install -r requirements.txt
echo ''
