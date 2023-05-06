#!/bin/bash

set -e

# Activate the virtual environment
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
npm install -g aws-cdk


cdk destroy --force
python3 delete_resource.py
