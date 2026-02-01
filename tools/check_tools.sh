#!/bin/bash
# Tools 目录检查脚本

echo "🔍 Tools 目录脱敏和整合检查"
echo "========================================"
echo ""

cd "$(dirname "$0")"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "📂 目录结构"
echo "-----------------------------------------"
echo ""
echo "核心工具（已通用化，可直接使用）："
ls -1 *.py *.json *.md 2>/dev/null | grep -v "^examples$" | sed 's/^/  ✅ /'
echo ""
echo "参考实现（需要自定义）："
ls -1 examples/ 2>/dev/null | sed 's/^/  ⚠️  /'
echo ""

echo "🔒 脱敏检查"
echo "-----------------------------------------"
echo ""

# 检查核心工具
personal_info=0
for file in wiznote_to_obsidian.py fix_p0_issues.py config_helper.py; do
    count=$(grep -c '/Users/wardlu\|智布互联\|唯衣网络' "$file" 2>/dev/null || echo "0")
    if [ "$count" -gt "0" ]; then
        echo -e "${YELLOW}⚠️  $file: $count 处个人信息${NC}"
        personal_info=$((personal_info + count))
    else
        echo -e "${GREEN}✅ $file: 已脱敏${NC}"
    fi
done

echo ""
echo "📊 统计信息"
echo "-----------------------------------------"
echo ""
echo "核心工具："
core_count=$(ls -1 *.py 2>/dev/null | wc -l | xargs)
echo "  数量: $core_count"
echo "  总大小: $(du -sh . | awk '{print $1}')"
echo ""
echo "参考实现："
example_count=$(ls -1 examples/ 2>/dev/null | wc -l | xargs)
echo "  数量: $example_count"
echo "  总大小: $(du -sh examples/ | awk '{print $1}')"
echo ""

if [ $personal_info -eq 0 ]; then
    echo -e "${GREEN}✅ 核心工具已完全脱敏和通用化${NC}"
    echo ""
    echo "推荐使用："
    echo "  1. wiznote_to_obsidian.py - 主工具（整合所有功能）"
    echo "  2. fix_p0_issues.py - P0 问题修复"
    echo ""
    echo "参考实现位于 examples/ 目录，需要自定义后使用"
else
    echo -e "${YELLOW}⚠️  发现 $personal_info 处个人信息${NC}"
    echo "需要进一步清理"
fi
