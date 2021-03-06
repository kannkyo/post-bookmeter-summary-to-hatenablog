#!/bin/bash

FUNCTION_NAME=post-bookmeter-summary-to-hatenablog

rm -f lambda.zip

pushd src
    zip -rq ../lambda.zip .
popd

aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://lambda.zip
