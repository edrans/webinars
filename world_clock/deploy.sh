#!/bin/bash 

REGION=${1-'us-east-1'}

export FUNCTION_NAME=$(basename "$PWD")
echo "Zipping directory"
zip -qr ../deployment.zip ./sdk/lib/python3.6/site-packages ./lambda_function.py

echo "Deploying lambda function ${FUNCTION_NAME}"
aws lambda update-function-code --function-name ${FUNCTION_NAME} --zip-file fileb://../deployment.zip --region $REGION
echo "Done!"
