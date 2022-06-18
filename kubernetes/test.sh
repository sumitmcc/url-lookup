#!/bin/bash

for i in $(eval echo {1..2000})
do
  curl -X GET http://127.0.0.1:8080/api/1/test/hello > /dev/null 2>&1
done
