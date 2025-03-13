#!/bin/bash

# 启动 Solara 应用并在后台运行，输出重定向到日志文件
solara run --port 8765 ./src/demo_02.py > solara_demo02_output.log 2>&1 &
SOLARA_PID=$!

# 等待应用启动，最多 60 秒
echo "等待 Solara 应用demo02启动..."
for i in {1..60}; do
  # 使用 curl 检查应用是否返回 HTTP 200 状态码
  if curl -s -o /dev/null -w "%{http_code}" http://localhost:8765 | grep -q "200"; then
    echo "demo02 应用启动成功，返回 HTTP 200 状态码"
    # 优雅地停止应用
    kill -SIGTERM $SOLARA_PID
    wait $SOLARA_PID
    echo "demo02 应用已优雅地停止"
    exit 0
  fi
  sleep 1
done

# 如果超时，输出错误信息和日志
echo "错误：demo02 应用未在 60 秒内启动或未返回 HTTP 200 状态码"
cat solara_demo02_output.log
exit 1