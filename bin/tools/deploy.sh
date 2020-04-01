./bin/local/dist.sh

aws lambda update-function-code --function-name threading_tests \
--zip-file fileb://dist/aws-lambda-threading-example-python.zip
