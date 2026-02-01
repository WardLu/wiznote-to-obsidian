#!/usr/bin/env python3
"""
通用配置模块 - 供所有工具脚本使用
支持环境变量、配置文件、命令行参数
"""
import os
import json
from pathlib import Path
from typing import Optional, Dict


class ToolConfig:
    """工具配置类"""

    def __init__(self, config_file: Optional[str] = None):
        """初始化配置

        Args:
            config_file: 配置文件路径（JSON格式）
        """
        # 默认配置
        self.defaults = {
            'source_dir': self._expand_path('~/wiznote_export'),
            'vault_dir': self._expand_path('~/ObsidianVault'),
            'target_dir': None,  # 会自动设置为 vault_dir/02_Areas
            'attachments_dir': None,  # 会自动设置为 vault_dir/Wiznote/attachments
        }

        # 从配置文件加载
        if config_file and Path(config_file).exists():
            self._load_from_file(config_file)

        # 从环境变量加载（优先级最高）
        self._load_from_env()

        # 设置自动计算的路径
        if not self.target_dir:
            self.target_dir = os.path.join(self.vault_dir, '02_Areas')
        if not self.attachments_dir:
            self.attachments_dir = os.path.join(self.vault_dir, 'Wiznote/attachments')

    def _expand_path(self, path: str) -> str:
        """扩展路径中的 ~ 和环境变量"""
        return os.path.expanduser(os.path.expandvars(path))

    def _load_from_file(self, config_file: str):
        """从 JSON 文件加载配置"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                for key, value in config.items():
                    if hasattr(self, key):
                        setattr(self, key, self._expand_path(value))
        except Exception as e:
            print(f"⚠️  无法加载配置文件 {config_file}: {e}")

    def _load_from_env(self):
        """从环境变量加载配置"""
        env_mapping = {
            'WIZNOTE_SOURCE_DIR': 'source_dir',
            'WIZNOTE_VAULT_DIR': 'vault_dir',
            'WIZNOTE_TARGET_DIR': 'target_dir',
            'WIZNOTE_ATTACHMENTS_DIR': 'attachments_dir',
        }

        for env_key, attr_name in env_mapping.items():
            value = os.getenv(env_key)
            if value:
                setattr(self, attr_name, self._expand_path(value))

    def validate(self) -> bool:
        """验证配置是否有效"""
        errors = []

        # 检查必需的目录
        if not Path(self.vault_dir).exists():
            errors.append(f"Vault 目录不存在: {self.vault_dir}")

        if not Path(self.target_dir).exists():
            errors.append(f"目标目录不存在: {self.target_dir}")

        if errors:
            print("❌ 配置验证失败：")
            for error in errors:
                print(f"  - {error}")
            return False

        return True

    def __str__(self) -> str:
        """返回配置摘要"""
        return f"""ToolConfig:
  source_dir: {self.source_dir}
  vault_dir: {self.vault_dir}
  target_dir: {self.target_dir}
  attachments_dir: {self.attachments_dir}"""


# 全局配置实例
_global_config: Optional[ToolConfig] = None


def get_config(config_file: Optional[str] = None) -> ToolConfig:
    """获取全局配置实例"""
    global _global_config
    if _global_config is None:
        _global_config = ToolConfig(config_file)
    return _global_config


def reset_config():
    """重置全局配置"""
    global _global_config
    _global_config = None


if __name__ == '__main__':
    # 测试配置
    import sys

    config_file = sys.argv[1] if len(sys.argv) > 1 else None
    config = get_config(config_file)

    print(config)
    print("\n验证配置:")
    if config.validate():
        print("✅ 配置有效")
    else:
        print("❌ 配置无效")
