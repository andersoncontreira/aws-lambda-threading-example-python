python3 -m venv venv
source ./venv/bin/activate

if [ "$1" = "--port" ]
then
  PORT=$2
fi
if [ -z "$PORT" ]
then
  PORT=8000
fi
# chalice local --port $PORT
