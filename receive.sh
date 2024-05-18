#!/bin/bash

PORT=12345
echo "Listening on UDP port ${PORT}"

# 监听UDP端口，接收数据并打印
nc -lu 127.0.0.1 $PORT