#!/usr/bin/env python3
"""
同步删除工具 - 安全地同步两个目录的删除操作

⚠️ 安全特性：
1. 不会自动删除，必须人工确认
2. 执行前显示完整的删除清单
3. 显示两边文件的映射关系
4. 生成删除日志，可追溯
5. 支持干运行模式（只显示，不删除）

使用流程：
1. 运行扫描：python3 sync_deletions.py --scan
2. 查看报告：review 删除清单
3. 确认删除：python3 sync_deletions.py --confirm
4. 查看日志：cat sync_delete_YYYYMMDD_HHMMSS.log
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime
import difflib


class SyncDeletionTool:
    """同步删除工具"""

    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir).expanduser().resolve()
        self.target_dir = Path(target_dir).expanduser().resolve()
        self.source_files: Dict[str, Path] = {}
        self.target_files: Dict[str, Path] = {}
        self.to_delete: List[Dict] = []
        self.scan_report_file = Path(".sync_delete_scan_report.json")

    def scan_files(self, directory: Path, pattern: str = "*.md") -> Dict[str, Path]:
        """扫描目录中的所有 Markdown 文件"""
        files = {}
        for file_path in directory.rglob(pattern):
            # 使用相对于根目录的路径作为键
            rel_path = file_path.relative_to(directory)
            files[str(rel_path)] = file_path
        return files

    def find_matching_file(self, source_rel_path: str, source_name: str) -> Tuple[Path, float]:
        """在目标目录中查找匹配的文件

        策略：
        1. 精确匹配相对路径
        2. 文件名模糊匹配
        3. 目录结构模糊匹配
        """
        # 策略 1: 精确匹配相对路径
        if source_rel_path in self.target_files:
            return self.target_files[source_rel_path], 1.0

        # 策略 2: 文件名匹配
        source_path = Path(source_rel_path)
        source_filename = source_path.name

        candidates = []
        for target_rel, target_path in self.target_files.items():
            target_filename = Path(target_rel).name

            if source_filename == target_filename:
                # 文件名相同，检查路径相似度
                source_parts = source_rel_path.replace(os.sep, '/').split('/')
                target_parts = target_rel.replace(os.sep, '/').split('/')

                # 计算路径相似度
                path_similarity = difflib.SequenceMatcher(None, source_rel_path, target_rel).ratio()

                candidates.append((target_path, path_similarity))

        # 按相似度排序
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0]

        return None, 0.0

    def scan_deletions(self) -> Dict:
        """扫描需要删除的文件"""
        print(f"🔍 扫描删除差异...")
        print(f"源目录: {self.source_dir}")
        print(f"目标目录: {self.target_dir}\n")

        # 扫描两边的文件
        print("📂 扫描源目录文件...")
        self.source_files = self.scan_files(self.source_dir)
        print(f"   找到 {len(self.source_files)} 个文件\n")

        print("📂 扫描目标目录文件...")
        self.target_files = self.scan_files(self.target_dir)
        print(f"   找到 {len(self.target_files)} 个文件\n")

        # 找出需要删除的文件
        print("🔍 分析文件差异...\n")

        for source_rel, source_path in self.source_files.items():
            # 检查源文件是否存在（如果不存在，说明已被删除）
            if not source_path.exists():
                target_file, similarity = self.find_matching_file(source_rel, source_path.name)

                if target_file and target_file.exists():
                    deletion_item = {
                        'source_rel_path': source_rel,
                        'source_file': str(source_path),
                        'target_file': str(target_file),
                        'target_rel_path': str(target_file.relative_to(self.target_dir)),
                        'similarity': similarity,
                        'reason': '源文件已删除',
                        'status': 'pending'
                    }
                    self.to_delete.append(deletion_item)

        # 生成报告
        report = {
            'scan_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'source_dir': str(self.source_dir),
            'target_dir': str(self.target_dir),
            'source_files_count': len(self.source_files),
            'target_files_count': len(self.target_files),
            'to_delete_count': len(self.to_delete),
            'deletions': self.to_delete
        }

        return report

    def display_report(self, report: Dict):
        """显示删除报告"""
        print("=" * 80)
        print("📋 同步删除报告")
        print("=" * 80)
        print()

        print(f"📊 统计信息")
        print(f"   扫描时间: {report['scan_time']}")
        print(f"   源目录文件数: {report['source_files_count']}")
        print(f"   目标目录文件数: {report['target_files_count']}")
        print(f"   需要删除的文件: {report['to_delete_count']}")
        print()

        if report['to_delete_count'] == 0:
            print("✅ 没有需要同步删除的文件")
            return

        print("⚠️  需要删除的文件清单")
        print("-" * 80)

        for i, item in enumerate(report['deletions'], 1):
            print(f"\n{i}. {item['target_rel_path']}")
            print(f"   源文件: {item['source_rel_path']}")
            print(f"   映射关系: {item['source_rel_path']} → {item['target_rel_path']}")
            print(f"   相似度: {item['similarity']:.1%}")
            print(f"   原因: {item['reason']}")

        print()
        print("=" * 80)
        print("⚠️  警告：以上文件将被删除！")
        print("=" * 80)
        print()

    def save_report(self, report: Dict):
        """保存扫描报告"""
        with open(self.scan_report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"📄 扫描报告已保存到: {self.scan_report_file}")

    def load_report(self) -> Dict:
        """加载扫描报告"""
        if not self.scan_report_file.exists():
            print(f"❌ 找不到扫描报告: {self.scan_report_file}")
            print(f"   请先运行: python3 sync_deletions.py --scan")
            return None

        with open(self.scan_report_file, 'r', encoding='utf-8') as f:
            report = json.load(f)

        return report

    def confirm_deletion(self) -> bool:
        """确认删除操作"""
        print("=" * 80)
        print("⚠️  确认删除操作")
        print("=" * 80)
        print()

        response = input("你已查看删除清单，确认要删除这些文件吗？(yes/no): ").strip().lower()

        return response in ['yes', 'y']

    def execute_deletions(self, report: Dict) -> Dict:
        """执行删除操作"""
        if not report['deletions']:
            print("✅ 没有需要删除的文件")
            return {'success': True, 'deleted_count': 0, 'log_file': None}

        print()
        print("🗑️  开始删除文件...")
        print()

        # 创建删除日志
        log_file = Path(f"sync_delete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

        deleted_count = 0
        failed_count = 0

        with open(log_file, 'w', encoding='utf-8') as log:
            log.write(f"同步删除日志\n")
            log.write(f"{'=' * 80}\n")
            log.write(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write(f"源目录: {report['source_dir']}\n")
            log.write(f"目标目录: {report['target_dir']}\n")
            log.write(f"计划删除: {len(report['deletions'])} 个文件\n")
            log.write(f"{'=' * 80}\n\n")

            for item in report['deletions']:
                target_file = Path(item['target_file'])

                try:
                    if target_file.exists():
                        # 先备份到 .trash 目录
                        trash_dir = self.target_dir / ".sync_delete_trash"
                        trash_dir.mkdir(exist_ok=True)

                        import shutil
                        backup_path = trash_dir / target_file.name
                        counter = 1
                        while backup_path.exists():
                            backup_path = trash_dir / f"{target_file.name}_{counter}"
                            counter += 1

                        shutil.move(str(target_file), str(backup_path))

                        log.write(f"✅ 已删除: {item['target_rel_path']}\n")
                        log.write(f"   备份到: {backup_path}\n")
                        log.write(f"   源文件: {item['source_rel_path']}\n\n")

                        deleted_count += 1
                        print(f"   ✅ {item['target_rel_path']}")

                    else:
                        log.write(f"⚠️  文件不存在: {item['target_rel_path']}\n\n")
                        failed_count += 1

                except Exception as e:
                    log.write(f"❌ 删除失败: {item['target_rel_path']}\n")
                    log.write(f"   错误: {e}\n\n")
                    failed_count += 1
                    print(f"   ❌ {item['target_rel_path']}: {e}")

        log.write(f"\n{'=' * 80}\n")
        log.write(f"删除完成: 成功 {deleted_count} 个，失败 {failed_count} 个\n")

        print()
        print(f"📊 删除完成")
        print(f"   成功: {deleted_count} 个")
        print(f"   失败: {failed_count} 个")
        print(f"   日志: {log_file}")
        print(f"   备份目录: {self.target_dir / '.sync_delete_trash'}")

        return {
            'success': True,
            'deleted_count': deleted_count,
            'failed_count': failed_count,
            'log_file': str(log_file)
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='同步删除工具 - 安全地同步两个目录的删除操作',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 1. 扫描差异（只查看，不删除）
  python3 sync_deletions.py --scan \\
    --source ~/wiznote_export \\
    --target ~/ObsidianVault

  # 2. 查看报告后，确认删除
  python3 sync_deletions.py --confirm

  # 3. 恢复删除的文件（从 .trash 目录）
  # 删除的文件已备份到: target_dir/.sync_delete_trash/

⚠️ 安全提示:
  - 默认使用 --scan 模式，只查看不删除
  - 必须明确使用 --confirm 才会执行删除
  - 所有删除操作都会先备份到 .trash 目录
  - 删除操作会生成详细日志，可追溯
        """
    )

    parser.add_argument('--source', required=True, help='源目录（你手动删除笔记的目录）')
    parser.add_argument('--target', required=True, help='目标目录（需要同步删除的 Obsidian Vault）')
    parser.add_argument('--scan', action='store_true', help='扫描模式：只查看差异，不删除')
    parser.add_argument('--confirm', action='store_true', help='确认删除：执行删除操作')

    args = parser.parse_args()

    # 创建工具实例
    tool = SyncDeletionTool(args.source, args.target)

    # 扫描模式
    if args.scan:
        print("🔍 扫描模式（只查看，不删除）\n")
        report = tool.scan_deletions()
        tool.display_report(report)
        tool.save_report(report)

        if report['to_delete_count'] > 0:
            print()
            print("💡 下一步：")
            print("   1. 仔细查看上面的删除清单")
            print("   2. 确认无误后，运行以下命令执行删除：")
            print(f"      python3 {Path(__file__).name} --confirm")
            print(f"      --source {args.source}")
            print(f"      --target {args.target}")
        return

    # 确认删除模式
    if args.confirm:
        print("⚠️  确认删除模式\n")

        # 加载扫描报告
        report = tool.load_report()
        if not report:
            return

        # 显示报告
        tool.display_report(report)

        if report['to_delete_count'] == 0:
            return

        # 确认删除
        if tool.confirm_deletion():
            result = tool.execute_deletions(report)

            # 删除扫描报告
            if result['success']:
                tool.scan_report_file.unlink()
                print(f"\n✅ 已删除扫描报告")

        else:
            print("\n❌ 取消删除操作")

        return

    # 没有指定模式，显示帮助
    parser.print_help()


if __name__ == '__main__':
    main()
