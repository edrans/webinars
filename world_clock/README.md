# The World Clock skill

This skill is an example for using Python and the Alexa SDK. (ASK). It implements two intents (actions):

1. Get local time
1. Get time in city

## How to install Alexa SDK?

```
apt install python pip3

virtualenv sdk
source sdk/bin/activate

pip3 install ask-sdk

```

## How to include the ASK


*lambda_function.py*

```
import sys
sys.path.append('sdk/lib/python3.6/site-packages/')

from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()


def lambda_handler(event, context):
    # TODO implement
    return 'Hello from Lambda'

```

## How to create a lambda function?

You can create the lambda function using the AWS console or use the provided `create.sh` script:

```
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

```

## Deployment

To deploy new code you can zip all in file a file and upload it to S3 or use the AWS CLI, or use the `deploy.sh` script:

```
#!/bin/bash 

REGION=${1-'us-east-1'}

export FUNCTION_NAME=$(basename "$PWD")
echo "Zipping directory"
zip -qr ../deployment.zip ./sdk/lib/python3.6/site-packages ./lambda_function.py

echo "Deploying lambda function ${FUNCTION_NAME}"
aws lambda update-function-code --function-name ${FUNCTION_NAME} --zip-file fileb://../deployment.zip --region $REGION
echo "Done!
```

# Implementing the skill 

In the `lambda_function.py` file you will find the logic for a world clock function, which handles the *World Clock* skill's intents: 

* `getTime`:  Get the local time (UTC)
* `getCityTime` Get the local time in a given city

# Model file

The `es_MX.json` file has the utterances in Spanish for the intents.  You can load this file in the developer console.
