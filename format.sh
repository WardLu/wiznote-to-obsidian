#!/bin/bash
# WizNote 格式化工具快捷脚本

cd "$(dirname "$0")"

echo "🚀 运行 WizNote 格式化工具..."
python3 tools/obsidian_formatter.py --config config_wiznote_download.json "$@"
