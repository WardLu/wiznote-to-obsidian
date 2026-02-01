#!/usr/bin/env python3
"""
为 Obsidian 文档添加增强特性：关键词高亮、Callouts、折叠块
"""
import re
from pathlib import Path

def enhance_b2b_book_notes(file_path):
    """增强《决胜B端》读书笔记"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 关键词高亮规则
    highlights = [
        (r'作为一名B端产品经理', '作为一名==B端产品经理=='),
        (r'深度访谈', '==深度访谈=='),
        (r'轮岗实习', '==轮岗实习=='),
        (r'调研问卷', '==调研问卷=='),
        (r'数据分析', '==数据分析=='),
        (r'行业研究', '==行业研究=='),
        (r'业务调研', '==业务调研=='),
        (r'只有投身于一线', '==只有投身于一线==，才能深刻地理解业务，做出正确的决策'),
        (r'幸存者偏差', '==幸存者偏差=='),
        (r'诱导性问题', '==诱导性问题=='),
    ]

    # 应用关键词高亮
    for pattern, replacement in highlights:
        content = re.sub(pattern, replacement, content)

    # 为重要引语添加 Callout（处理转义字符）
    content = re.sub(
        r'\\*\\*==只有投身于一线==.*?\\*\\*',
        '> [!QUOTE]\n> ==只有投身于一线==，才能深刻地理解业务，做出正确的决策。\n> 产品经理要当一个冲在前线的人，而不是在后方拍脑袋的人。',
        content,
        flags=re.DOTALL
    )

    # 为深度访谈注意事项添加折叠块
    interview_notes = r'==深度访谈==需要准备好访谈大纲、从高级别人员开始访谈、提前研究访谈对象、和访谈对象保持联系。'
    details_block = '''<details>
<summary>📋 深度访谈的注意事项</summary>

- 准备好访谈大纲
- 从高级别人员开始访谈
- 提前研究访谈对象
- 和访谈对象保持联系

</details>'''

    if interview_notes in content:
        content = content.replace(interview_notes, details_block)

    # 为调研问卷设计添加 Callout
    callout_pattern = r'线上的调研问卷是比较灵活的调研手段.*?多么让人崩溃的事情。'
    match = re.search(callout_pattern, content, re.DOTALL)
    if match:
        original_text = match.group(0)
        callout_text = f'''> [!TIP]
> 线上的==调研问卷==是比较灵活的调研手段，既可以进行定性分析，也可以进行定量分析，并且很容易推广。
>
> ⚠️ **注意**：问卷的内容设计一定要谨慎，因为一旦问卷发出，就无法修改问题了。'''
        content = content.replace(original_text, callout_text)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def enhance_interview_notes(file_path):
    """增强面试材料"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 关键词高亮
    highlights = [
        (r'商业论证阶段', '==商业论证阶段=='),
        (r'产品设计阶段', '==产品设计阶段=='),
        (r'SaaS产品指标', '==SaaS产品指标=='),
        (r'需求收集', '==需求收集=='),
        (r'竞品分析', '==竞品分析=='),
    ]

    for pattern, replacement in highlights:
        content = re.sub(pattern, replacement, content)

    # 为核心方法论添加 Callout
    content = re.sub(
        r'(####产品设计方法论\n)',
        r'\1\n> [!IMPORTANT]\n> 产品设计需要系统的方法论支撑，以下是从商业论证到产品落地的完整流程。\n',
        content
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    print("🎨 开始增强 Obsidian 文档...")

    # 增强《决胜B端》读书笔记
    b2b_file = Path("/Users/wardlu/Documents/Obsidian Vault/02_Areas/产品思考/B端产品/决胜B端读书笔记.md")
    if b2b_file.exists():
        if enhance_b2b_book_notes(b2b_file):
            print(f"✅ 已增强：决胜B端读书笔记.md")
    else:
        print(f"❌ 文件不存在：{b2b_file}")

    # 增强面试材料
    interview_file = Path("/Users/wardlu/Documents/Obsidian Vault/02_Areas/求职/Wiznote面试材料/2025高级产品经理面试.md")
    if interview_file.exists():
        if enhance_interview_notes(interview_file):
            print(f"✅ 已增强：2025高级产品经理面试.md")
    else:
        print(f"❌ 文件不存在：{interview_file}")

    print("\n🎉 增强完成！")
    print("   - 添加了关键词高亮（==关键词==）")
    print("   - 添加了 Callouts（重要提示）")
    print("   - 添加了折叠块（详细信息）")

if __name__ == '__main__':
    main()
