#!/bin/bash
# 快速验证转换结果

echo "=================================================="
echo "🔍 WizNote → Obsidian 快速验证"
echo "=================================================="
echo ""

echo "📊 文件统计:"
echo "   - Markdown 文件: $(find "/Users/wardlu/Documents/Obsidian Vault/02_Areas" -name "*.md" -type f | wc -l | xargs)"
echo "   - 图片文件: $(find "/Users/wardlu/Documents/Obsidian Vault/Wiznote/attachments/all_images" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" \) 2>/dev/null | wc -l | xargs)"
echo ""

echo "🖼️  图片路径检查:"
img_links=$(grep -r "/Wiznote/attachments/all_images/" "/Users/wardlu/Documents/Obsidian Vault/02_Areas" --include="*.md" | wc -l | xargs)
echo "   - 图片链接数量: $img_links"
echo ""

echo "✨ 增强特性检查:"
highlights=$(grep -r "==" "/Users/wardlu/Documents/Obsidian Vault/02_Areas" --include="*.md" | grep -o '==[^=]*==' | wc -l | xargs)
callouts=$(grep -r "> \[!" "/Users/wardlu/Documents/Obsidian Vault/02_Areas" --include="*.md" | wc -l | xargs)
echo "   - 关键词高亮: $highlights 处"
echo "   - Callouts: $callouts 个"
echo ""

echo "🔍 问题检查:"
double_ext=$(find "/Users/wardlu/Documents/Obsidian Vault/02_Areas" -name "*.md.md" -type f | wc -l | xargs)
relative_path=$(grep -r "](images/" "/Users/wardlu/Documents/Obsidian Vault/02_Areas" --include="*.md" | wc -l | xargs)
echo "   - 双重扩展名: $double_ext 个"
echo "   - 相对路径残留: $relative_path 个"
echo ""

echo "📋 核心文件验证:"
if [ -f "/Users/wardlu/Documents/Obsidian Vault/02_Areas/产品思考/B端产品/决胜B端读书笔记.md" ]; then
    echo "   ✅ 决胜B端读书笔记.md"
    grep -q "==" "/Users/wardlu/Documents/Obsidian Vault/02_Areas/产品思考/B端产品/决胜B端读书笔记.md" && echo "      - 包含关键词高亮" || echo "      - ⚠️  缺少关键词高亮"
    grep -q "> \[!" "/Users/wardlu/Documents/Obsidian Vault/02_Areas/产品思考/B端产品/决胜B端读书笔记.md" && echo "      - 包含 Callouts" || echo "      - ⚠️  缺少 Callouts"
    grep -q "/Wiznote/attachments/all_images/" "/Users/wardlu/Documents/Obsidian Vault/02_Areas/产品思考/B端产品/决胜B端读书笔记.md" && echo "      - 图片路径已更新" || echo "      - ⚠️  图片路径未更新"
fi

if [ -f "/Users/wardlu/Documents/Obsidian Vault/02_Areas/求职/Wiznote面试材料/2025高级产品经理面试.md" ]; then
    echo "   ✅ 2025高级产品经理面试.md"
    grep -q "==" "/Users/wardlu/Documents/Obsidian Vault/02_Areas/求职/Wiznote面试材料/2025高级产品经理面试.md" && echo "      - 包含关键词高亮" || echo "      - ⚠️  缺少关键词高亮"
    grep -q "> \[!" "/Users/wardlu/Documents/Obsidian Vault/02_Areas/求职/Wiznote面试材料/2025高级产品经理面试.md" && echo "      - 包含 Callouts" || echo "      - ⚠️  缺少 Callouts"
fi

echo ""
echo "=================================================="
echo "✅ 验证完成！"
echo "=================================================="
echo ""
echo "💡 下一步:"
echo "   1. 在 Obsidian 中打开 '决胜B端读书笔记.md'"
echo "   2. 检查图片是否正常显示"
echo "   3. 验证高亮和 Callout 是否生效"
echo ""
