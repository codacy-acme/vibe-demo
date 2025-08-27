#!/bin/bash
docker build -t app .
docker run -d -p 3008:3008 --name app app
sleep 5
mkdir -p zap_output
chmod 777 zap_output
docker run --rm -v $(pwd)/zap_output:/zap/wrk --add-host=host.docker.internal:host-gateway ghcr.io/zaproxy/zaproxy:stable zap-full-scan.py -t http://host.docker.internal:3008 -J /zap/wrk/zap_report.json
docker stop app
docker rm app
