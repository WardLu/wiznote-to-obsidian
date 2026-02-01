#!/bin/bash
# 开源前检查脚本 - 验证脱敏和通用化

echo "🔍 WizNote to Obsidian - 开源前检查"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查结果
check_count=0
pass_count=0
fail_count=0

# 检查函数
check() {
    local name="$1"
    local command="$2"

    check_count=$((check_count + 1))
    echo -n "[$check_count] $name ... "

    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
        pass_count=$((pass_count + 1))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        fail_count=$((fail_count + 1))
        return 1
    fi
}

warn() {
    local name="$1"
    local command="$2"

    check_count=$((check_count + 1))
    echo -n "[$check_count] $name ... "

    if eval "$command" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  WARNING${NC}"
        return 1
    else
        echo -e "${GREEN}✅ PASS${NC}"
        pass_count=$((pass_count + 1))
        return 0
    fi
}

# 进入项目目录
cd "$(dirname "$0")"

echo "📂 检查项目结构"
echo "-----------------------------------------"

check "Python 主工具存在" "test -f tools/wiznote_to_obsidian.py"
check "配置模块存在" "test -f tools/config_helper.py"
check "配置模板存在" "test -f tools/config.example.json"
check "README 存在" "test -f README.md"
check "LICENSE 存在" "test -f LICENSE"
check "Git 忽略文件存在" "test -f .gitignore"

echo ""
echo "🔒 检查敏感信息"
echo "-----------------------------------------"

warn "无个人路径 (wardlu)" "! grep -r '/Users/wardlu' tools/*.py README.md"
warn "无公司名称 (智布互联)" "! grep -r '智布互联' tools/*.py README.md 2>/dev/null"
warn "无配置文件 (config.json)" "! test -f tools/config.json"
warn "归档目录已忽略" "grep -q 'archive_reports/' .gitignore"

echo ""
echo "🧪 检查工具可用性"
echo "-----------------------------------------"

check "主工具可执行" "python3 tools/wiznote_to_obsidian.py --help"
check "配置模块可导入" "python3 -c 'from tools.config_helper import ToolConfig; print(\"OK\")' 2>/dev/null || python3 tools/config_helper.py"

echo ""
echo "📋 检查文档完整性"
echo "-----------------------------------------"

check "README 包含使用说明" "grep -q '快速开始' README.md"
check "README 包含配置说明" "grep -q '配置' README.md"
check "LICENSE 是 MIT" "grep -q 'MIT' LICENSE"

echo ""
echo "========================================"
echo "📊 检查结果汇总"
echo "========================================"
echo ""
echo -e "总计: ${check_count} 项检查"
echo -e "${GREEN}通过: ${pass_count}${NC}"
echo -e "${RED}失败: ${fail_count}${NC}"
echo ""

if [ $fail_count -eq 0 ]; then
    echo -e "${GREEN}✅ 所有检查通过！可以安全上传到 GitHub${NC}"
    echo ""
    echo "下一步："
    echo "  1. git init"
    echo "  2. git add ."
    echo "  3. git commit -m 'feat: 初始化项目'"
    echo "  4. 在 GitHub 创建仓库"
    echo "  5. git remote add origin <仓库地址>"
    echo "  6. git push -u origin main"
    exit 0
else
    echo -e "${RED}❌ 存在问题，请先修复后再上传${NC}"
    echo ""
    echo "建议操作："
    echo "  1. 查看上述失败的检查项"
    echo "  2. 根据 脱敏通用化总结.md 进行修改"
    echo "  3. 重新运行此脚本"
    exit 1
fi
