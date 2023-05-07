#!/bin/bash

set -e

# when error occurred, run cleanup function
function cleanup {
    echo "An error occurred. Running 'cdk destroy' to clean up resources."
    cdk destroy --force

    # cdk destroyで削除されないリソースを削除
    python3 delete_resource.py

    # workflowを削除
    python3 delete_workflow.py
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
python3 set_workflow.py --workflow-file .github/workflows/build_template.yaml
python3 delete_workflow.py

# update cdk
cdk deploy --require-approval never

python3 set_workflow.py --workflow-file .github/workflows/deploy_template.yaml
