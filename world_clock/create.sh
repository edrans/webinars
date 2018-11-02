#!/bin/bash 

REGION=${1-'us-east-1'}
RUNTIME="python3.6"
ROLE="arn:aws:iam::555555555555:role/lambda_basic_execution_worldclock"
HANDLER="lambda_function.lambda_handler"

export FUNCTION_NAME=$(basename "$PWD")
echo "Zipping directory"
zip -qr ../deployment.zip ./sdk/lib/python3.6/site-packages ./lambda_function.py

echo "Creating lambda function ${FUNCTION_NAME}"
aws lambda create-function --function-name ${FUNCTION_NAME} --runtime ${RUNTIME} --role ${ROLE} --handler ${HANDLER} --zip-file fileb://../deployment.zip --region ${REGION}
echo "Done!"
