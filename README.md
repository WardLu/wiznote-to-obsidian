# WizNote to Obsidian

<div align="center">

# 🚀 一体化迁移工具

**让你的 WizNote 笔记完美迁移到 Obsidian**

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/WardLu/wiznote-to-obsidian?style=social)](https://github.com/WardLu/wiznote-to-obsidian/stargazers)

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [安装指南](#-安装指南) • [使用文档](#-使用文档) • [贡献指南](#️-贡献指南)

</div>

---

## ✨ 项目简介

**WizNote to Obsidian** 是一个强大的迁移工具，帮助你将 WizNote（为知笔记）导出的 Markdown 文件完整迁移到 Obsidian，并建立结构化的知识管理体系。

### 🎯 核心价值

- 🚀 **一键迁移** - 完整自动化流程，从导出到整合
- 🔧 **智能修复** - 自动修复 300+ Markdown 语法问题
- 🖼️ **图片迁移** - 统一管理 3000+ 张图片
- 🔗 **链接转换** - 自动转换为 Obsidian WikiLinks
- ✨ **格式增强** - 添加元数据、高亮、Callouts
- 📊 **完整报告** - 详细的统计和分析报告

### 📊 实际验证

本工具已在生产环境验证：
- ✅ 成功迁移 **400+ 文件**
- ✅ 修复 **300+ 格式问题**
- ✅ 迁移 **3000+ 张图片**
- ✅ 建立 **知识图谱** (MOC)

---

## 🌟 功能特性

### 核心功能

| 功能 | 说明 |
|:------|:------|
| 📝 **智能迁移** | 自动识别并迁移 WizNote 导出的 Markdown 文件 |
| 🔧 **格式修复** | 自动修复标题、列表、代码块等 7 类格式问题 |
| 🔗 **链接转换** | Markdown 链接 → Obsidian WikiLinks |
| 🖼️ **图片管理** | 统一图片路径，支持本地和远程图片 |
| 📎 **附件迁移** | 迁移 PDF、XMind、Excel 等附件文件 |
| 🔗 **附件链接** | 自动为笔记添加附件引用链接 |
| ✨ **元数据增强** | 自动添加 YAML front matter |
| 📊 **质量报告** | 生成详细的迁移报告和统计信息 |

### 支持的修复类型

- ✅ 标题格式（空格、层级跳跃）
- ✅ 列表格式（标记统一）
- ✅ 代码块（语言指定、fenced code）
- ✅ 链接（Markdown → WikiLinks）
- ✅ 图片路径（相对路径 → 绝对路径）
- ✅ 多余空行
- ✅ 粗体斜体格式

---

## 🎬 快速开始

### 前置要求

- Python 3.6 或更高版本
- WizNote 导出的 Markdown 文件
- Obsidian（可选，用于验证结果）

### 一键运行

```bash
# 1. 克隆项目
git clone https://github.com/WardLu/wiznote-to-obsidian.git
cd wiznote-to-obsidian

# 2. 配置路径（可选）
export WIZNOTE_VAULT_DIR=~/ObsidianVault

# 3. 执行迁移
cd tools
python3 wiznote_to_obsidian.py --all
```

### 配置说明

**方式 1：环境变量（推荐）**

```bash
export WIZNOTE_SOURCE_DIR=~/wiznote_export
export WIZNOTE_VAULT_DIR=~/ObsidianVault
```

**方式 2：配置文件**

```bash
cp tools/config.example.json tools/config.json
# 编辑 config.json
```

**方式 3：使用默认路径**

工具会自动使用以下默认路径：
- `source_dir`: `~/wiznote_export`
- `vault_dir`: `~/ObsidianVault`

---

## 📦 安装指南

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/WardLu/wiznote-to-obsidian.git
cd wiznote-to-obsidian

# 无需额外依赖，使用 Python 标准库
python3 --version  # 确保 Python 3.6+
```

### Docker 方式（可选）

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . /app
CMD ["python3", "tools/wiznote_to_obsidian.py", "--all"]
```

---

## 📖 使用文档

### 主工具使用

```bash
# 查看帮助
python3 wiznote_to_obsidian.py --help

# 执行完整流程（不包括附件）
python3 wiznote_to_obsidian.py --all

# 只检查语法
python3 wiznote_to_obsidian.py --check

# 只修复格式
python3 wiznote_to_obsidian.py --fix

# 只转换链接
python3 wiznote_to_obsidian.py --links

# 只修复图片
python3 wiznote_to_obsidian.py --images

# 迁移附件文件（重要！）
python3 wiznote_to_obsidian.py --migrate-attachments

# 为笔记添加附件链接（重要！）
python3 wiznote_to_obsidian.py --link-attachments

# 生成报告
python3 wiznote_to_obsidian.py --report
```

### 分步执行

```bash
# 1. 检查语法问题
python3 wiznote_to_obsidian.py --check > issues.txt

# 2. 修复格式问题
python3 wiznote_to_obsidian.py --fix

# 3. 转换链接
python3 wiznote_to_obsidian.py --links

# 4. 修复图片路径
python3 wiznote_to_obsidian.py --images

# 5. 迁移附件文件（新增）
python3 wiznote_to_obsidian.py --migrate-attachments

# 6. 为笔记添加附件链接（新增）
python3 wiznote_to_obsidian.py --link-attachments

# 7. 生成报告
python3 wiznote_to_obsidian.py --report
```

### ⚠️ 附件迁移（重要）

WizNote 导出时，附件（PDF、XMind、Excel 等）不会自动链接到笔记中。需要执行以下步骤：

1. **迁移附件文件** - 将所有附件从导出目录复制到 Obsidian Vault
2. **添加附件链接** - 自动为笔记添加附件引用

```bash
# 迁移附件（约 70MB，包括 PDF、XMind、Excel 等）
python3 wiznote_to_obsidian.py --migrate-attachments

# 自动为笔记添加附件链接
python3 wiznote_to_obsidian.py --link-attachments
```

---

## 📸 迁移效果

### 迁移前后对比

| 维度 | WizNote 导出 | Obsidian 整合后 |
|:-----|:------------|:---------------|
| 文件结构 | 分散的文件 | 结构化的 PARA 体系 |
| 链接方式 | 标准 Markdown 链接 | WikiLinks 双向链接 |
| 格式增强 | 单纯 Markdown | 增强的 Obsidian 格式 |
| 元数据 | 无 | 完整的 YAML front matter |

### 知识图谱

迁移后自动建立知识图谱，支持：

- 🔗 **双向链接** - 自动关联相关笔记
- 🏷️ **标签系统** - 结构化标签体系
- 📊 **MOC 索引** - 内容地图索引
- 🔍 **图谱视图** - 可视化知识网络

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发指南

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细的贡献指南。

### 报告问题

请使用 [GitHub Issues](https://github.com/WardLu/wiznote-to-obsidian/issues) 报告问题或提出功能建议。

---

## 📜 开源协议

本项目采用 [MIT License](LICENSE) 开源许可证。

```
MIT License

Copyright (c) 2026 WardLu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
...
```

---

## 💖 打赏支持

如果这个项目对你有帮助，欢迎请我喝杯咖啡！☕

<table align="center">
  <tr>
    <td align="center" valign="middle">
      <img src="assets/sponsor/wechat.jpg" alt="微信支付" style="max-width: 200px;" />
      <div><strong>微信支付</strong></div>
    </td>
    <td align="center" valign="middle">
      <img src="assets/sponsor/alipay.jpg" alt="支付宝" style="max-width: 200px;" />
      <div><strong>支付宝</strong></div>
    </td>
    <td align="center" valign="middle">
      <a href="https://www.buymeacoffee.com/" target="_blank">
        <img src="assets/sponsor/buymeacoffee.png" alt="Buy Me a Coffee" style="max-width: 200px;" />
      </a>
      <div><strong>Buy Me a Coffee</strong></div>
    </td>
  </tr>
</table>

<div align="center">

**感谢您的支持！** 🙏

</div>

---

## 📞 联系方式

- **GitHub**: [@WardLu](https://github.com/WardLu)
- **Email**: [wardlu@126.com](mailto:wardlu@126.com)
- **项目主页**: https://github.com/WardLu/wiznote-to-obsidian

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WardLu/wiznote-to-obsidian&type=Date)](https://star-history.com/#WardLu/wiznote-to-obsidian&Date)

---

## 🔗 相关资源

- [Obsidian 官方文档](https://help.obsidian.md/)
- [WizNote 官网](https://www.wiznote.com/)
- [PARA 方法](https://fortelabs.co/blog/para/)
- [MOC 方法论](https://www.youtube.com/watch?v=AoHnrBSKEuY)

---

<div align="center">

**Made with ❤️ by [WardLu](https://github.com/WardLu)**

如果觉得有用，请给个 Star ⭐

</div>
