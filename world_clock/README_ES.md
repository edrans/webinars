# La skill Reloj Mundial 

Esta skill es un ejemplo de uso de Python y el SDK de Alexa (ASK). Esta implementa dos intents (acciones):

1. Dime la hora 
1. Dime la hora en tal ciudad

## ¿Cómo instalar el SDK de Alexa?

```
apt install python pip3

virtualenv sdk
source sdk/bin/activate

pip3 install ask-sdk
```

## ¿Cómo incluir ASK?


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

## ¿Cómo crear la función lambda?

Puedes crear la función lambda usando la conosla de AWS o usar el script `create.sh` proporcionado:


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

## Despliegue

Para desplegar nuevo código puedes colocar todo en un zip y subirlo a S3 o usar la CLI de AWS, o corer el script `deploy.sh`


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

# Implementando la skill

En el archivo `lambda_function.py` encontrarás la lógica de la función para el reloj mundial, el cual maneja los intents de la skill *Reloj Mundial*:


* `getTime`:  Da la hora local (UTC) 
* `getCityTime` Da la hora local en una ciudad

# Archivo Model

El archivo `es_MX.json`  tiene las frases en español para los intents. Puedes cargarlos desde la consola de Alexa si quieres ahorrar algo de tiempo.
