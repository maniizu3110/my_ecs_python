#!/bin/bash
cdk bootstrap 

cdk deploy --require-approval never

# replace app .env
python3 update_env.py

# push build file to repository
python3 build_image.py

# update cdk
cdk deploy --require-approval never
