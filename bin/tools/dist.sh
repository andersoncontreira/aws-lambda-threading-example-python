python3 -m pip install -r requirements.txt -t ./vendor
# ignora a pasta dist, venv, .git (as pastas vão ser criadas, porém seu conteúdo não)
zip -r dist/aws-lambda-threading-example-python.zip ./ -x ./venv/**\* ./bin/**\* ./dist/**\* ./.git/**\* ./.ideia/**\* \
README.md LICENSE .gitignore