#!/bin/bash

set -e

# when error occurred, run cleanup function
function cleanup {
    echo "An error occurred. Running 'cdk destroy' to clean up resources."
    cdk destroy --force
    python3 delete_resource.py
}


# Activate the virtual environment
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
npm install -g aws-cdk


cdk bootstrap

cdk deploy --require-approval never

trap cleanup ERR

# replace app .env with created aws resources information
python3 update_env.py

# create workflow and commit to github for build image to ecr
python3 set_workflow.py

# update cdk
cdk deploy --require-approval never


## 構築に必要な情報を配列で持てば、複数の環境を構築できる
# cluster名をカタログで持つ
# inputからcluster名を取得
# repository名は同じ場合も違う場合もある
# ->cluster名とrepository名/build-pathでユニークになる数だけ構築する
# 実際はどこをユニークして判別するか
# cluster名=s3bucket, key=repopository+build-path