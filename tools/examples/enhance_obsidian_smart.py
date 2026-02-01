#!/usr/bin/env python3
"""
智能增强 Obsidian 文档 - 避免重复替换
"""
import re
from pathlib import Path

def enhance_file_smartly(file_path, keywords, important_quotes):
    """智能增强文档，避免重复替换"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 记录原始内容用于对比
    original_content = content
    changes_made = []

    # 1. 关键词高亮（只高亮第一次出现）
    for keyword in keywords:
        # 避免重复高亮
        if f'=={keyword}==' not in content:
            pattern = re.compile(rf'\b{re.escape(keyword)}\b')
            match = pattern.search(content)
            if match:
                # 只替换第一个匹配项
                content = pattern.sub(f'=={keyword}==', content, count=1)
                changes_made.append(f"高亮关键词: {keyword}")

    # 2. 为重要引语添加 Callout
    for quote in important_quotes:
        if quote['text'] in content and quote['callout'] not in content:
            content = content.replace(quote['text'], quote['callout'])
            changes_made.append(f"添加 Callout: {quote['title']}")

    # 3. 为深度访谈添加折叠块
    interview_text = '深度访谈需要准备好访谈大纲、从高级别人员开始访谈、提前研究访谈对象、和访谈对象保持联系。'
    details_block = '''<details>
<summary>📋 深度访谈的注意事项</summary>

- 准备好访谈大纲
- 从高级别人员开始访谈
- 提前研究访谈对象
- 和访谈对象保持联系

</details>'''

    if interview_text in content and '<details>' not in content:
        content = content.replace(interview_text, details_block)
        changes_made.append("添加折叠块: 深度访谈注意事项")

    # 只在有修改时写入文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes_made
    return False, []

def main():
    print("🎨 智能增强 Obsidian 文档...")

    # 《决胜B端》的关键词
    b2b_keywords = [
        'B端产品经理',
        '深度访谈',
        '轮岗实习',
        '调研问卷',
        '业务调研',
        '幸存者偏差',
    ]

    # 《决胜B端》的重要引语
    b2b_quotes = [
        {
            'title': '投身一线',
            'text': '只有投身于一线，才能深刻地理解业务，做出正确的决策。产品经理要当一个冲在前线的人，而不是在后方拍脑袋的人。',
            'callout': '> [!QUOTE]\n> 只有投身于一线，才能深刻地理解业务，做出正确的决策。\n> 产品经理要当一个冲在前线的人，而不是在后方拍脑袋的人。'
        },
        {
            'title': '调研问卷',
            'text': '线上的调研问卷是比较灵活的调研手段，既可以进行定性分析，也可以进行定量分析，并且很容易推广。问卷的内容设计一定要谨慎，因为一旦问卷发出，就无法修改问题了，如果辛辛苦苦收回了大量反馈，却发现当初的问题设计不合理，是多么让人崩溃的事情。',
            'callout': '> [!TIP]\n> 线上的==调研问卷==是比较灵活的调研手段，既可以进行定性分析，也可以进行定量分析，并且很容易推广。\n>\n> ⚠️ **注意**：问卷的内容设计一定要谨慎，因为一旦问卷发出，就无法修改问题了。'
        }
    ]

    # 面试材料的关键词
    interview_keywords = [
        '商业论证',
        '产品设计',
        '需求收集',
        '竞品分析',
        'SaaS',
    ]

    # 面试材料的 Callout
    interview_callout = {
        'title': '产品设计方法论',
        'text': '####产品设计方法论',
        'callout': '####产品设计方法论\n\n> [!IMPORTANT]\n> 产品设计需要系统的方法论支撑，以下是从商业论证到产品落地的完整流程。'
    }

    # 增强《决胜B端》
    b2b_file = Path("/Users/wardlu/Documents/Obsidian Vault/02_Areas/产品思考/B端产品/决胜B端读书笔记.md")
    if b2b_file.exists():
        # 先读取原始文件内容（因为之前可能已被修改）
        with open(b2b_file, 'r', encoding='utf-8') as f:
            current_content = f.read()

        # 如果已经被破坏，需要手动修复
        if '====' in current_content:
            print(f"⚠️  检测到文件已被破坏，正在修复...")
            # 移除重复的等号
            current_content = re.sub(r'==+', '==', current_content)
            # 修复混乱的 Callout
            current_content = re.sub(
                r'\\*\\*==> \[!QUOTE\].*?\n>.*?\n>.*?\\\*\\*',
                '> [!QUOTE]\n> ==只有投身于一线==，才能深刻地理解业务，做出正确的决策。\n> 产品经理要当一个冲在前线的人，而不是在后方拍脑袋的人。',
                current_content,
                flags=re.DOTALL
            )
            with open(b2b_file, 'w', encoding='utf-8') as f:
                f.write(current_content)
            print(f"✅ 已修复文件")

        enhanced, changes = enhance_file_smartly(b2b_file, b2b_keywords, b2b_quotes)
        if enhanced:
            print(f"✅ 增强完成：决胜B端读书笔记.md")
            for change in changes:
                print(f"   - {change}")
        else:
            print(f"ℹ️  文件已是最新状态：决胜B端读书笔记.md")

    # 增强面试材料
    interview_file = Path("/Users/wardlu/Documents/Obsidian Vault/02_Areas/求职/Wiznote面试材料/2025高级产品经理面试.md")
    if interview_file.exists():
        with open(interview_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 添加 Callout
        if interview_callout['text'] in content and interview_callout['callout'] not in content:
            content = content.replace(interview_callout['text'], interview_callout['callout'])
            with open(interview_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 增强完成：2025高级产品经理面试.md")
            print(f"   - 添加 Callout: 产品设计方法论")

        # 高亮关键词
        changes = []
        for keyword in interview_keywords:
            if f'=={keyword}==' not in content:
                pattern = re.compile(rf'\b{re.escape(keyword)}\b')
                if pattern.search(content):
                    content = pattern.sub(f'=={keyword}==', content, count=1)
                    changes.append(f"高亮关键词: {keyword}")

        if changes:
            with open(interview_file, 'w', encoding='utf-8') as f:
                f.write(content)
            for change in changes:
                print(f"   - {change}")

    print("\n🎉 智能增强完成！")

if __name__ == '__main__':
    main()
