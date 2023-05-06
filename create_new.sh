#!/bin/bash

set -e

function cleanup {
    echo "An error occurred. Running 'cdk destroy' to clean up resources."
    cdk destroy --force
}

trap cleanup ERR

# Activate the virtual environment
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
npm install -g aws-cdk

# Install the dependencies
pip install -r requirements.txt

cdk bootstrap

cdk deploy --require-approval never

# replace app .env
python3 update_env.py

# push build file to repository
python3 build_image.py

# update cdk
cdk deploy --require-approval never
