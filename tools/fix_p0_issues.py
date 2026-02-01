#!/usr/bin/env python3
"""
P0 问题修复工具 - 通用的关键问题检测和修复
支持自定义规则，适用于任何 Markdown 项目
"""
import re
import os
import argparse
from pathlib import Path
from typing import List, Dict, Callable


class P0IssueDetector:
    """P0 问题检测器"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.issues = []

    def detect_unclosed_bold_markers(self) -> List[Dict]:
        """检测未闭合的粗体标记"""
        issues = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                # 检查未闭合的 ** 标记
                bold_count = line.count('**')
                if bold_count % 2 != 0:
                    issues.append({
                        'line': i,
                        'type': '未闭合的粗体标记',
                        'severity': 'ERROR',
                        'content': line.strip(),
                        'fix_method': '检查并在适当位置添加 ** 闭合标记'
                    })
        except Exception as e:
            print(f"⚠️  无法读取文件 {self.file_path}: {e}")

        return issues

    def detect_heading_level_skips(self) -> List[Dict]:
        """检测标题层级跳跃"""
        issues = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            prev_level = 0
            heading_pattern = re.compile(r'^(#{1,6})\s*(.*?)\s*$')

            for i, line in enumerate(lines, 1):
                match = heading_pattern.match(line)
                if not match:
                    continue

                level = len(match.group(1))

                # 检测标题层级跳跃（超过1级）
                if prev_level > 0 and level > prev_level + 1:
                    issues.append({
                        'line': i,
                        'type': '标题层级跳跃',
                        'severity': 'WARNING',
                        'content': line.strip(),
                        'from': f'H{prev_level}',
                        'to': f'H{level}',
                        'suggested': f'H{prev_level + 1}',
                        'fix_method': f'建议将 H{level} 改为 H{prev_level + 1}'
                    })

                prev_level = level
        except Exception as e:
            print(f"⚠️  无法读取文件 {self.file_path}: {e}")

        return issues

    def detect_all(self) -> List[Dict]:
        """检测所有 P0 问题"""
        self.issues = []
        self.issues.extend(self.detect_unclosed_bold_markers())
        self.issues.extend(self.detect_heading_level_skips())
        return self.issues


class P0IssueFixer:
    """P0 问题修复器"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.backup_path = Path(str(file_path) + '.bak')

    def backup(self):
        """备份原文件"""
        import shutil
        shutil.copy2(self.file_path, self.backup_path)

    def fix_heading_level(self, line_num: int, new_level: int):
        """修复标题层级"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if line_num < 1 or line_num > len(lines):
                return False

            # 修改标题层级
            line = lines[line_num - 1]
            match = re.match(r'^(#{1,6})\s*(.*?)\s*$', line)
            if match:
                new_heading = '#' * new_level + ' ' + match.group(2) + '\n'
                lines[line_num - 1] = new_heading

                with open(self.file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                return True
        except Exception as e:
            print(f"❌ 修复失败: {e}")
            return False

    def restore_backup(self):
        """恢复备份"""
        import shutil
        if self.backup_path.exists():
            shutil.copy2(self.backup_path, self.file_path)
            print(f"✅ 已恢复备份: {self.file_path}")


def scan_directory(directory: str, patterns: List[str] = None) -> Dict[str, List[Dict]]:
    """扫描目录中的所有 Markdown 文件"""
    dir_path = Path(directory)
    all_issues = {}

    # 查找所有 .md 文件
    md_files = list(dir_path.rglob('*.md'))

    # 如果指定了模式，过滤文件
    if patterns:
        filtered_files = []
        for pattern in patterns:
            filtered_files.extend(dir_path.rglob(pattern))
        md_files = filtered_files

    print(f"🔍 扫描 {len(md_files)} 个文件...\n")

    for file_path in md_files:
        detector = P0IssueDetector(str(file_path))
        issues = detector.detect_all()

        if issues:
            rel_path = str(file_path.relative_to(dir_path))
            all_issues[rel_path] = issues

    return all_issues


def generate_fix_guide(issues: Dict[str, List[Dict]], output_file: str = None):
    """生成修复指南"""
    guide = []

    guide.append("# 🚨 P0 问题修复指南\n")
    guide.append("本文档由工具自动生成，包含所有需要手动修复的 P0 问题。\n")
    guide.append("---\n\n")

    # 统计
    total_issues = sum(len(issue_list) for issue_list in issues.values())
    error_count = sum(1 for issue_list in issues.values()
                     for issue in issue_list if issue['severity'] == 'ERROR')
    warning_count = sum(1 for issue_list in issues.values()
                       for issue in issue_list if issue['severity'] == 'WARNING')

    guide.append("## 📊 问题统计\n\n")
    guide.append(f"- **总问题数**: {total_issues}\n")
    guide.append(f"- **🔴 ERROR**: {error_count}\n")
    guide.append(f"- **🟡 WARNING**: {warning_count}\n")
    guide.append(f"- **涉及文件**: {len(issues)}\n\n")

    guide.append("---\n\n")

    # 详细问题列表
    guide.append("## 📋 详细问题列表\n\n")

    for idx, (file_path, issue_list) in enumerate(issues.items(), 1):
        guide.append(f"### 问题 {idx}: {file_path}\n\n")

        for issue in issue_list:
            severity_emoji = {'ERROR': '🔴', 'WARNING': '🟡'}.get(issue['severity'], '🔵')
            guide.append(f"{severity_emoji} **第 {issue['line']} 行** - {issue['type']}\n\n")
            guide.append(f"**内容**: `{issue['content']}`\n\n")

            if 'suggested' in issue:
                guide.append(f"**当前**: {issue['from']}\n")
                guide.append(f"**建议**: {issue['suggested']}\n\n")

            guide.append(f"**修复方法**: {issue['fix_method']}\n\n")
            guide.append("---\n\n")

    # 修复建议
    guide.append("## 🔧 修复建议\n\n")
    guide.append("### 自动修复（需谨慎）\n\n")
    guide.append("部分问题可以使用工具自动修复：\n\n")
    guide.append("```bash\n")
    guide.append("# 修复标题层级问题\n")
    guide.append("python3 wiznote_to_obsidian.py --fix\n")
    guide.append("```\n\n")

    guide.append("### 手动修复\n\n")
    guide.append("1. 在编辑器中打开文件\n")
    guide.append("2. 跳转到指定行\n")
    guide.append("3. 根据修复方法进行调整\n")
    guide.append("4. 保存文件\n\n")

    guide.append("### 验证修复\n\n")
    guide.append("修复后重新运行扫描：\n\n")
    guide.append("```bash\n")
    guide.append("python3 fix_p0_issues.py --dir /path/to/vault\n")
    guide.append("```\n\n")

    guide_content = ''.join(guide)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        print(f"✅ 修复指南已保存到: {output_file}")

    return guide_content


def main():
    parser = argparse.ArgumentParser(
        description='P0 问题检测和修复工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 扫描目录
  python3 fix_p0_issues.py --dir /path/to/vault

  # 只扫描特定文件
  python3 fix_p0_issues.py --dir /path/to/vault --pattern "*产品*.md"

  # 生成修复指南
  python3 fix_p0_issues.py --dir /path/to/vault --output fix_guide.md

  # 交互式修复
  python3 fix_p0_issues.py --dir /path/to/vault --interactive
        """
    )

    parser.add_argument('--dir', required=True, help='要扫描的目录路径')
    parser.add_argument('--pattern', action='append', help='文件名模式（可多次使用）')
    parser.add_argument('--output', help='输出修复指南到文件')
    parser.add_argument('--interactive', action='store_true', help='交互式修复模式')
    parser.add_argument('--fix', nargs=2, metavar=('LINE', 'LEVEL'),
                       help='修复指定行的标题层级（行号 新层级）')

    args = parser.parse_args()

    # 扫描目录
    issues = scan_directory(args.dir, args.pattern)

    if not issues:
        print("✅ 未发现 P0 问题！")
        return

    # 生成修复指南
    guide = generate_fix_guide(issues, args.output)

    if not args.output:
        print(guide)

    # 交互式修复
    if args.interactive:
        print("\n" + "=" * 60)
        print("🔧 交互式修复模式")
        print("=" * 60)

        for file_path, issue_list in issues.items():
            print(f"\n📄 文件: {file_path}")

            for issue in issue_list:
                if issue['type'] == '标题层级跳跃':
                    print(f"  第 {issue['line']} 行: {issue['from']} → {issue['to']}")
                    choice = input(f"  是否修复为 {issue['suggested']}? (y/n): ")

                    if choice.lower() == 'y':
                        full_path = Path(args.dir) / file_path
                        fixer = P0IssueFixer(str(full_path))
                        fixer.backup()
                        new_level = int(issue['suggested'][1])  # 提取层级数字
                        if fixer.fix_heading_level(issue['line'], new_level):
                            print(f"  ✅ 已修复")
                        else:
                            print(f"  ❌ 修复失败")

    # 命令行修复
    if args.fix:
        line_num, new_level = int(args.fix[0]), int(args.fix[1])
        # 这里需要指定具体文件，暂时略过
        print(f"修复模式：第 {line_num} 行改为 H{new_level}")


if __name__ == '__main__':
    main()
