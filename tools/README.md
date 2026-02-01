# Tools 目录说明

## 📁 目录结构

```
tools/
├── wiznote_to_obsidian.py     🔧 主工具（推荐使用）
├── fix_p0_issues.py           🔧 P0 问题修复
├── config_helper.py           📦 配置模块
├── config.example.json        📝 配置模板
├── 工具使用说明.md             📖 使用文档
│
└── examples/                  💡 参考实现（需要自定义）
    ├── add_front_matter.py
    ├── enhance_obsidian.py
    ├── enhance_obsidian_smart.py
    └── ... (其他工具)
```

## 🚀 快速开始

### 使用主工具（推荐）

```bash
# 执行完整流程
python3 wiznote_to_obsidian.py --all

# 查看帮助
python3 wiznote_to_obsidian.py --help
```

### 使用配置文件

```bash
# 复制配置模板
cp config.example.json config.json

# 编辑配置
vim config.json

# 使用配置文件
python3 wiznote_to_obsidian.py --config config.json --all
```

## 🛠️ 工具说明

### 核心工具（已通用化）

| 工具 | 大小 | 功能 | 状态 |
|------|------|------|------|
| `wiznote_to_obsidian.py` | 21KB | 一体化迁移工具 | ✅ 可直接使用 |
| `fix_p0_issues.py` | 10KB | P0 问题检测和修复 | ✅ 可直接使用 |
| `config_helper.py` | 3.8KB | 通用配置模块 | ✅ 可直接使用 |

### 参考实现（需要自定义）

`examples/` 目录包含 10 个专项工具，它们：
- ✅ 提供功能参考
- ⚠️  包含硬编码路径
- ⚠️  需要根据需求修改

**注意**：主工具已整合这些功能，建议优先使用主工具。

## 📖 详细文档

完整使用说明请参考：[工具使用说明.md](./工具使用说明.md)

## ⚙️ 配置说明

### 环境变量（推荐）

```bash
export WIZNOTE_SOURCE_DIR=~/wiznote_export
export WIZNOTE_VAULT_DIR=~/ObsidianVault
```

### 配置文件

```bash
cp config.example.json config.json
# 编辑 config.json
```

## 🔍 常见问题

**Q: 什么时候需要使用 examples/ 中的工具？**

A: 大多数情况下不需要。主工具已整合所有核心功能。examples/ 中的工具适用于：
- 需要自定义特定功能
- 学习工具实现细节
- 作为二次开发的参考

**Q: 如何自定义 examples/ 中的工具？**

A:
1. 复制工具到主目录
2. 修改硬编码的路径
3. 使用 `config_helper.py` 管理配置
4. 测试工具功能
