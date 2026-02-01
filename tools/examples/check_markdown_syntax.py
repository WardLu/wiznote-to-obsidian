#!/usr/bin/env python3
"""
Markdown 语法检查工具
检查 Obsidian Vault 中的 Markdown 文件语法问题
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

class MarkdownChecker:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.issues = []
        self.lines = []

    def check(self) -> List[Dict]:
        """执行所有检查"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.lines = f.readlines()
        except Exception as e:
            return [{
                'type': '文件读取错误',
                'line': 0,
                'severity': 'ERROR',
                'message': str(e)
            }]

        # 执行各项检查
        self.check_headings()
        self.check_lists()
        self.check_code_blocks()
        self.check_bold_italic()
        self.check_links()
        self.check_blockquotes()
        self.check_horizontal_rules()
        self.check_tables()
        self.check_blank_lines()

        return self.issues

    def check_headings(self):
        """检查标题层级和格式"""
        prev_level = 0
        heading_pattern = re.compile(r'^(#{1,6})\s*(.*?)\s*$')

        for i, line in enumerate(self.lines, 1):
            match = heading_pattern.match(line)
            if not match:
                continue

            level = len(match.group(1))
            text = match.group(2)

            # 检查标题前后空格
            if line.startswith('#') and not line.startswith('# '):
                self.issues.append({
                    'type': '标题格式',
                    'line': i,
                    'severity': 'WARNING',
                    'message': f'标题后缺少空格: {line.strip()}'
                })

            # 检查标题层级跳跃
            if prev_level > 0 and level > prev_level + 1:
                self.issues.append({
                    'type': '标题层级',
                    'line': i,
                    'severity': 'WARNING',
                    'message': f'标题层级跳跃: H{prev_level} → H{level} (建议: H{prev_level + 1})'
                })

            prev_level = level

    def check_lists(self):
        """检查列表格式"""
        in_list = False
        list_indent = 0

        for i, line in enumerate(self.lines, 1):
            # 检查无序列表
            if re.match(r'^(\s*)([*\-])\s+', line):
                indent = len(line) - len(line.lstrip())
                marker = line.strip()[0]

                if marker == '*':
                    self.issues.append({
                        'type': '列表格式',
                        'line': i,
                        'severity': 'INFO',
                        'message': f'建议使用 "-" 代替 "*" 作为无序列表标记'
                    })

            # 检查有序列表
            if re.match(r'^(\s*)\d+\.\s+', line):
                pass  # 格式正确

    def check_code_blocks(self):
        """检查代码块格式"""
        in_code_block = False
        code_fence_pattern = re.compile(r'^```(\w*)')

        for i, line in enumerate(self.lines, 1):
            match = code_fence_pattern.match(line)

            if match:
                in_code_block = not in_code_block
                lang = match.group(1)

                # 检查是否指定语言
                if in_code_block and not lang:
                    self.issues.append({
                        'type': '代码块',
                        'line': i,
                        'severity': 'INFO',
                        'message': '代码块未指定语言 (建议: ```python、```javascript 等)'
                    })

            # 检查缩进代码块 (4空格)
            if line.startswith('    ') and not line.startswith('   \n'):
                if not in_code_block:
                    self.issues.append({
                        'type': '代码块',
                        'line': i,
                        'severity': 'WARNING',
                        'message': '发现缩进代码块 (建议使用 ``` 包裹)'
                    })

    def check_bold_italic(self):
        """检查粗体和斜体格式"""
        # 检查非标准的粗体斜体
        for i, line in enumerate(self.lines, 1):
            # 检查 __粗体__ (不标准)
            if re.search(r'__(?!_)', line) and re.search(r'__', line):
                self.issues.append({
                    'type': '粗体格式',
                    'line': i,
                    'severity': 'INFO',
                    'message': '建议使用 **粗体** 代替 __粗体__'
                })

            # 检查未闭合的标记
            bold_count = line.count('**')
            italic_count = line.count('*') - bold_count * 2

            if bold_count % 2 != 0:
                self.issues.append({
                    'type': '未闭合标记',
                    'line': i,
                    'severity': 'ERROR',
                    'message': '可能存在未闭合的 ** 粗体标记'
                })

    def check_links(self):
        """检查内部链接"""
        # 检查 Markdown 链接
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')

        for i, line in enumerate(self.lines, 1):
            matches = link_pattern.findall(line)

            for text, path in matches:
                self.issues.append({
                    'type': '内部链接',
                    'line': i,
                    'severity': 'INFO',
                    'message': f'可转换为 WikiLinks: [{text}]({path}) → [[{text}]]'
                })

    def check_blockquotes(self):
        """检查引用块格式"""
        in_blockquote = False

        for i, line in enumerate(self.lines, 1):
            if line.startswith('>'):
                in_blockquote = True
            elif in_blockquote and line.strip():
                # 引用块结束后应该有空行
                if not line.startswith('>'):
                    in_blockquote = False

    def check_horizontal_rules(self):
        """检查水平线格式"""
        hr_pattern = re.compile(r'^(\*{3,}|-{3,}|_{3,})\s*$')

        for i, line in enumerate(self.lines, 1):
            if hr_pattern.match(line):
                # 检查前后是否有空行
                has_prev_blank = i > 1 and not self.lines[i-2].strip()
                has_next_blank = i < len(self.lines) and not self.lines[i].strip()

                if not has_prev_blank or not has_next_blank:
                    self.issues.append({
                        'type': '水平线',
                        'line': i,
                        'severity': 'INFO',
                        'message': '水平线前后建议有空行'
                    })

    def check_tables(self):
        """检查表格格式"""
        in_table = False

        for i, line in enumerate(self.lines, 1):
            if '|' in line:
                # 检查是否是表格分隔线
                if re.match(r'^\|?(\s*:?-+:?\s*\|)+\s*:?-+:?\s*\|?$', line):
                    in_table = True
                elif in_table and '|' in line:
                    # 在表格中
                    pass
            elif in_table and line.strip():
                in_table = False

    def check_blank_lines(self):
        """检查空行"""
        consecutive_blanks = 0

        for i, line in enumerate(self.lines, 1):
            if not line.strip():
                consecutive_blanks += 1
            else:
                if consecutive_blanks > 2:
                    self.issues.append({
                        'type': '多余空行',
                        'line': i - consecutive_blanks,
                        'severity': 'INFO',
                        'message': f'发现 {consecutive_blanks} 个连续空行 (建议: 最多2个)'
                    })
                consecutive_blanks = 0


def check_all_files(directory: str) -> Dict:
    """检查目录下所有 Markdown 文件"""
    dir_path = Path(directory)

    # 查找所有 .md 文件
    md_files = list(dir_path.rglob('*.md'))

    results = {
        'total_files': len(md_files),
        'issues_by_file': defaultdict(list),
        'issues_by_type': defaultdict(int),
        'issues_by_severity': defaultdict(int)
    }

    for file_path in md_files:
        checker = MarkdownChecker(str(file_path))
        issues = checker.check()

        if issues:
            results['issues_by_file'][str(file_path)] = issues

            for issue in issues:
                results['issues_by_type'][issue['type']] += 1
                results['issues_by_severity'][issue['severity']] += 1

    return results


def main():
    """主函数"""
    target_dir = '/Users/wardlu/Documents/Obsidian Vault/02_Areas'

    print('🔍 开始扫描 Markdown 文件...\n')

    results = check_all_files(target_dir)

    print(f'📊 扫描完成！共检查 {results["total_files"]} 个文件\n')
    print('=' * 80)

    # 按严重程度统计
    print('\n📈 问题统计 (按严重程度):')
    print('-' * 80)
    severity_order = ['ERROR', 'WARNING', 'INFO']
    for severity in severity_order:
        count = results['issues_by_severity'].get(severity, 0)
        if count > 0:
            emoji = {'ERROR': '🔴', 'WARNING': '🟡', 'INFO': '🔵'}[severity]
            print(f'{emoji} {severity:10} {count:5} 个')

    # 按类型统计
    print('\n📈 问题统计 (按类型):')
    print('-' * 80)
    sorted_types = sorted(results['issues_by_type'].items(), key=lambda x: x[1], reverse=True)
    for issue_type, count in sorted_types:
        print(f'• {issue_type:15} {count:5} 个')

    # 详细问题列表
    print('\n📋 详细问题列表 (按文件分组):')
    print('=' * 80)

    sorted_files = sorted(results['issues_by_file'].items())
    for file_path, issues in sorted_files:
        # 只显示相对路径
        rel_path = file_path.replace('/Users/wardlu/Documents/Obsidian Vault/', '')
        print(f'\n📄 {rel_path}')
        print(f'   共 {len(issues)} 个问题\n')

        # 按严重程度分组显示
        for severity in severity_order:
            severity_issues = [i for i in issues if i['severity'] == severity]
            if severity_issues:
                emoji = {'ERROR': '🔴', 'WARNING': '🟡', 'INFO': '🔵'}[severity]
                print(f'   {emoji} {severity}')
                for issue in severity_issues[:5]:  # 每个文件最多显示5个
                    print(f'      第 {issue["line"]:3} 行: {issue["message"]}')
                if len(severity_issues) > 5:
                    print(f'      ... 还有 {len(severity_issues) - 5} 个 {severity} 问题')

    # 修复建议
    print('\n' + '=' * 80)
    print('🔧 修复建议:')
    print('-' * 80)

    print('\n✅ 可批量修复的问题:')
    print('   1. 标题前后空格 (使用 sed 或 Python 脚本)')
    print('   2. 无序列表标记统一 (用 - 代替 *)')
    print('   3. 多余空行清理')

    print('\n⚠️  需要手动修复的问题:')
    print('   1. 标题层级调整 (需要人工判断内容逻辑)')
    print('   2. 代码块语言指定 (需要识别代码类型)')
    print('   3. 内部链接转换为 WikiLinks (需要确认链接有效性)')

    print('\n📊 优先级建议:')
    print('   P0 (立即修复): 标题层级混乱、未闭合标记')
    print('   P1 (尽量修复): 列表格式、代码块语言')
    print('   P2 (时间允许): 粗体斜体统一、空行规范')

    print('\n' + '=' * 80)


if __name__ == '__main__':
    main()
