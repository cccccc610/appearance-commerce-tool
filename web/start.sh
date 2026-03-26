#!/bin/bash
# 外观商业化思考小工具 - 网页版启动脚本

echo "🎨 外观商业化思考小工具 v2.0 - 网页版"
echo "======================================"
echo ""

PORT=${1:-8080}

cd "$(dirname "$0")"

echo "📡 启动HTTP服务器..."
echo "📍 服务地址: http://localhost:${PORT}"
echo ""
echo "💡 使用方式:"
echo "   - 直接用浏览器打开 index.html 文件（推荐）"
echo "   - 或访问上述地址"
echo ""
echo "⏹  按 Ctrl+C 停止服务"
echo ""

python3 -m http.server $PORT --bind 0.0.0.0
