# WizNote to Obsidian

<div align="center">

# 🚀 一体化迁移工具

**从 WizNote 完美迁移到 Obsidian 的完整解决方案**

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/WardLu/wiznote-to-obsidian?style=social)](https://github.com/WardLu/wiznote-to-obsidian/stargazers)

[功能特性](#-核心功能) • [快速开始](#-快速开始) • [使用指南](#-使用指南) • [工具说明](#-工具说明) • [常见问题](#-常见问题)

</div>

---

## ✨ 项目简介

**WizNote to Obsidian** 是一套完整的迁移工具链，帮助你将 WizNote（为知笔记）无缝迁移到 Obsidian。项目包含两个核心工具：

1. **在线下载工具** (`WizNote_Migration/wiz_to_obsidian.py`) - 直接从 WizNote 云端下载笔记
2. **离线迁移工具** (`tools/wiznote_to_obsidian.py`) - 处理已导出的 Markdown 文件

### 🎯 核心价值

- 🌐 **在线下载** - 直接从 WizNote 云端获取笔记，无需手动导出
- 🔧 **智能修复** - 自动修复 Markdown 语法问题
- 🖼️ **图片管理** - 统一管理所有图片资源
- 📎 **附件迁移** - 完整迁移 PDF、XMind、Excel 等附件
- 🔗 **链接转换** - 自动转换为 Obsidian WikiLinks
- 🗑️ **同步删除** - 安全地同步删除操作
- ✨ **格式增强** - 添加元数据、优化格式
- 📊 **完整报告** - 详细的迁移统计和分析报告

### 📊 实际验证

本工具已在生产环境验证：
- ✅ 成功迁移 **400+ 文件**
- ✅ 修复 **300+ 格式问题**
- ✅ 迁移 **3000+ 张图片**
- ✅ 处理 **70MB+ 附件**
- ✅ 建立 **知识图谱** (MOC)

---

## 🌟 核心功能

### 在线下载工具 (`WizNote_Migration/wiz_to_obsidian.py`)

直接从 WizNote 云端下载笔记并转换为 Markdown 格式。

**功能特性：**
- 🌐 直接登录 WizNote 账号下载笔记
- 📁 保持原始文件夹结构
- 📝 自动转换 HTML → Markdown
- 🖼️ 下载笔记中的图片
- 🔄 递归扫描所有文件夹
- 💾 支持 Fallback 模式（纯文本提取）

**使用场景：**
- 需要从 WizNote 云端直接下载笔记
- 没有本地导出的 Markdown 文件
- 希望一次性下载所有笔记

### 离线迁移工具 (`tools/wiznote_to_obsidian.py`)

处理已导出的 Markdown 文件，优化格式并适配 Obsidian。

**功能特性：**
- 🔍 **语法检查** - 检测标题、列表、代码块等 7 类问题
- 🔧 **格式修复** - 自动修复常见 Markdown 语法错误
- 🔗 **链接转换** - Markdown 链接 → Obsidian WikiLinks
- 🖼️ **图片修复** - 统一图片路径，修复失效链接
- 📎 **附件迁移** - 迁移 PDF、XMind、Excel 等附件文件
- 🔗 **附件链接** - 自动为笔记添加附件引用
- ✨ **元数据增强** - 添加 YAML front matter
- 📊 **质量报告** - 生成详细的迁移报告和统计信息

### 辅助工具 (`tools/`)

| 工具 | 功能 | 使用场景 |
|:------|:------|:---------|
| `sync_deletions.py` | 安全同步删除操作 | 在两个目录间同步删除的文件 |
| `migrate_attachments.py` | 附件文件迁移 | 将附件从导出目录迁移到 Vault |
| `link_attachments.py` | 附件链接修复 | 为笔记自动添加附件引用 |
| `auto_fix_p0.py` | 自动修复 P0 问题 | 修复最严重的格式问题 |
| `fix_heading_levels.py` | 标题层级修复 | 修复标题层级跳跃问题 |
| `config_helper.py` | 配置管理助手 | 帮助生成和管理配置文件 |

### 支持的修复类型

- ✅ 标题格式（空格、层级跳跃）
- ✅ 列表格式（标记统一）
- ✅ 代码块（语言指定、fenced code）
- ✅ 链接（Markdown → WikiLinks）
- ✅ 图片路径（相对路径优化）
- ✅ 多余空行
- ✅ 粗体斜体格式

---

## 🎬 快速开始

### 前置要求

- Python 3.6 或更高版本
- WizNote 账号（用于在线下载）或已导出的 Markdown 文件
- Obsidian（可选，用于验证结果）

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/WardLu/wiznote-to-obsidian.git
cd wiznote-to-obsidian

# 安装 Python 依赖（仅在线下载工具需要）
pip3 install requests markdownify
```

### 方法一：在线下载（推荐）

如果你还没有导出 Markdown 文件，可以直接从 WizNote 云端下载：

```bash
# 进入在线下载工具目录
cd WizNote_Migration

# 运行下载工具
python3 wiz_to_obsidian.py

# 按提示输入 WizNote 账号和密码
# 下载的笔记将保存在 obsidian_export/ 目录
```

**在线下载工具详细说明：**

- **功能**：直接登录 WizNote 云端，下载所有笔记并转换为 Markdown
- **输出**：`obsidian_export/` 目录，保持原始文件夹结构
- **图片处理**：自动下载笔记中的图片，保存在 `{笔记名}_files/` 目录
- **Fallback 模式**：如果 ZIP 下载失败，会尝试纯文本提取（不含图片）

### 方法二：离线迁移

如果你已经有 WizNote 导出的 Markdown 文件：

```bash
# 1. 配置路径（可选）
export WIZNOTE_SOURCE_DIR=~/wiznote_export
export WIZNOTE_VAULT_DIR=~/ObsidianVault

# 2. 执行迁移
cd tools
python3 wiznote_to_obsidian.py --all
```

**离线迁移工具参数说明：**

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

# 干运行模式（不实际修改文件）
python3 wiznote_to_obsidian.py --fix --dry-run
```

### 配置说明

**方式 1：环境变量（推荐）**

```bash
export WIZNOTE_SOURCE_DIR=~/wiznote_export
export WIZNOTE_VAULT_DIR=~/ObsidianVault
export WIZNOTE_TARGET_DIR=~/ObsidianVault/02_Areas
export WIZNOTE_ATTACHMENTS_DIR=~/ObsidianVault/Wiznote/attachments
```

**方式 2：配置文件**

```bash
cd tools
cp config.example.json config.json
# 编辑 config.json，设置路径
```

**方式 3：使用默认路径**

工具会自动使用以下默认路径：
- `source_dir`: `~/wiznote_export`
- `vault_dir`: `~/ObsidianVault`
- `target_dir`: `~/ObsidianVault/02_Areas`
- `attachments_dir`: `~/ObsidianVault/Wiznote/attachments`

---

## 📖 使用指南

### 完整迁移流程

推荐的完整迁移流程：

```bash
# 步骤 1: 从 WizNote 云端下载笔记
cd WizNote_Migration
python3 wiz_to_obsidian.py
# 输入 WizNote 账号和密码
# 等待下载完成，笔记保存在 obsidian_export/

# 步骤 2: 使用离线迁移工具处理下载的笔记
cd ../tools

# 2.1 检查语法问题（可选）
python3 wiznote_to_obsidian.py --check

# 2.2 执行完整迁移流程
python3 wiznote_to_obsidian.py --all

# 步骤 3: 迁移附件（重要！）
# 3.1 迁移附件文件
python3 wiznote_to_obsidian.py --migrate-attachments

# 3.2 为笔记添加附件链接
python3 wiznote_to_obsidian.py --link-attachments

# 步骤 4: 生成最终报告
python3 wiznote_to_obsidian.py --report
```

### 分步执行详解

#### 1. 在线下载笔记

```bash
cd WizNote_Migration
python3 wiz_to_obsidian.py
```

**功能说明：**
- 直接登录 WizNote 云端
- 递归扫描所有文件夹
- 下载笔记并转换为 Markdown
- 自动处理图片和附件
- 支持 Fallback 模式（纯文本提取）

**输出结构：**
```
obsidian_export/
├── 文件夹1/
│   ├── 笔记1.md
│   ├── 笔记1_files/
│   │   └── image1.png
│   └── 笔记2.md
└── 文件夹2/
    └── 笔记3.md
```

#### 2. 语法检查

```bash
cd tools
python3 wiznote_to_obsidian.py --check
```

**检查项目：**
- 标题格式和层级
- 列表格式
- 代码块
- 粗体斜体
- 链接格式
- 空行

#### 3. 格式修复

```bash
python3 wiznote_to_obsidian.py --fix
```

**自动修复：**
- 标题前后空格
- 列表标记统一
- 多余空行
- 水平线格式

#### 4. 链接转换

```bash
python3 wiznote_to_obsidian.py --links
```

**转换示例：**
- `[笔记名](./笔记名.md)` → `[[笔记名]]`
- `[显示文本](./笔记名.md)` → `[[笔记名|显示文本]]`

#### 5. 图片修复

```bash
python3 wiznote_to_obsidian.py --images
```

**修复内容：**
- 统一图片路径
- 修复失效链接
- 优化相对路径

#### 6. 附件迁移

```bash
# 迁移附件文件（约 70MB，包括 PDF、XMind、Excel 等）
python3 wiznote_to_obsidian.py --migrate-attachments

# 自动为笔记添加附件链接
python3 wiznote_to_obsidian.py --link-attachments
```

**重要提示：** WizNote 导出时，附件不会自动链接到笔记中。需要执行以上两个步骤来完整迁移附件。

#### 7. 同步删除（可选）

如果你在 WizNote 导出目录中删除了笔记，可以同步删除 Obsidian Vault 中的对应文件：

```bash
# 步骤 1: 扫描差异（只查看，不删除）
python3 sync_deletions.py --scan \
  --source ~/wiznote_export \
  --target ~/ObsidianVault

# 步骤 2: 查看报告后，确认删除
python3 sync_deletions.py --confirm \
  --source ~/wiznote_export \
  --target ~/ObsidianVault
```

**安全特性：**
- 默认使用 `--scan` 模式，只查看不删除
- 必须明确使用 `--confirm` 才会执行删除
- 所有删除操作都会先备份到 `.trash` 目录
- 删除操作会生成详细日志，可追溯

---

## 🔧 工具说明

### 在线下载工具 (`WizNote_Migration/wiz_to_obsidian.py`)

**功能：** 直接从 WizNote 云端下载笔记并转换为 Markdown

**使用方法：**
```bash
cd WizNote_Migration
python3 wiz_to_obsidian.py
# 按提示输入 WizNote 账号和密码
```

**核心特性：**
- 直接登录 WizNote 账号服务器
- 递归扫描所有文件夹
- 自动转换 HTML → Markdown
- 下载笔记中的图片
- 支持 Fallback 模式（纯文本提取）

**输出目录：** `obsidian_export/`

### 离线迁移工具 (`tools/wiznote_to_obsidian.py`)

**功能：** 处理已导出的 Markdown 文件，优化格式并适配 Obsidian

**使用方法：**
```bash
cd tools
python3 wiznote_to_obsidian.py --all
```

**核心特性：**
- 语法检查和格式修复
- 链接转换为 WikiLinks
- 图片路径修复
- 附件迁移和链接
- 生成统计报告

### 同步删除工具 (`tools/sync_deletions.py`)

**功能：** 安全地同步两个目录的删除操作

**使用方法：**
```bash
# 步骤 1: 扫描差异（只查看，不删除）
python3 sync_deletions.py --scan \
  --source ~/wiznote_export \
  --target ~/ObsidianVault

# 步骤 2: 查看报告后，确认删除
python3 sync_deletions.py --confirm \
  --source ~/wiznote_export \
  --target ~/ObsidianVault
```

**安全特性：**
- 不会自动删除，必须人工确认
- 执行前显示完整的删除清单
- 显示两边文件的映射关系
- 生成删除日志，可追溯
- 支持干运行模式（只显示，不删除）

### 附件迁移工具 (`tools/migrate_attachments.py`)

**功能：** 将 WizNote 导出的附件迁移到 Obsidian Vault

**使用方法：**
```bash
python3 migrate_attachments.py \
  --export-dir ~/wiznote_export \
  --vault-dir ~/ObsidianVault
```

**支持附件类型：**
- PDF 文档
- XMind 思维导图
- Excel 表格
- PowerPoint 演示文稿
- 图片文件
- 其他文件

### 附件链接工具 (`tools/link_attachments.py`)

**功能：** 自动为笔记添加附件引用链接

**使用方法：**
```bash
python3 link_attachments.py \
  --export-dir ~/wiznote_export \
  --vault-dir ~/ObsidianVault
```

**智能匹配：**
- 根据文件名匹配附件
- 支持模糊匹配
- 按文件类型分组
- 自动添加附件链接区块

### 其他辅助工具

#### 自动修复 P0 问题 (`tools/auto_fix_p0.py`)

快速修复最严重的格式问题：

```bash
python3 auto_fix_p0.py
```

#### 标题层级修复 (`tools/fix_heading_levels.py`)

修复标题层级跳跃问题：

```bash
python3 fix_heading_levels.py
```

#### 配置助手 (`tools/config_helper.py`)

帮助生成和管理配置文件：

```bash
python3 config_helper.py
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
| 图片管理 | 本地路径 | 统一的附件目录 |
| 附件链接 | 无 | 自动添加附件引用 |

### 知识图谱

迁移后自动建立知识图谱，支持：

- 🔗 **双向链接** - 自动关联相关笔记
- 🏷️ **标签系统** - 结构化标签体系
- 📊 **MOC 索引** - 内容地图索引
- 🔍 **图谱视图** - 可视化知识网络

---

## ❓ 常见问题

### Q1: 在线下载工具无法登录？

**A:** 检查以下几点：
1. 确认 WizNote 账号和密码正确
2. 检查网络连接
3. 确认 WizNote 服务器地址（默认 `https://as.wiz.cn`）
4. 如果使用企业版，可能需要修改 `AS_URL`

### Q2: 下载的笔记中没有图片？

**A:** 在线下载工具提供了 Fallback 模式：
- 如果 ZIP 下载失败，会尝试纯文本提取（不含图片）
- 这通常是由于笔记格式特殊或权限问题
- 可以尝试在 WizNote 客户端中手动导出

### Q3: 附件迁移后找不到？

**A:** 检查以下几点：
1. 确认已运行 `--migrate-attachments`
2. 检查附件目录：`{vault_dir}/Wiznote/attachments/`
3. 运行 `--link-attachments` 添加附件链接
4. 查看附件清单：`{vault_dir}/Wiznote/attachments/附件清单.md`

### Q4: 同步删除工具误删文件怎么办？

**A:** 同步删除工具有多重保护：
1. 默认使用 `--scan` 模式，只查看不删除
2. 必须明确使用 `--confirm` 才会执行删除
3. 所有删除的文件都会备份到 `.sync_delete_trash/` 目录
4. 删除操作会生成详细日志
5. 如果误删，可以从备份目录恢复

### Q5: 链接转换后无法打开？

**A:** 检查以下几点：
1. 确认目标文件存在
2. 检查 WikiLinks 格式：`[[文件名]]` 或 `[[文件名|显示文本]]`
3. 确认文件名编码正确（避免特殊字符）
4. 在 Obsidian 中检查链接是否有效

### Q6: 如何验证迁移结果？

**A:** 推荐步骤：
1. 运行 `--check` 检查语法问题
2. 运行 `--report` 生成统计报告
3. 在 Obsidian 中打开 Vault
4. 检查几个随机笔记
5. 验证图片和附件链接
6. 查看图谱视图确认链接关系

### Q7: 如何处理迁移失败的笔记？

**A:** 检查以下几点：
1. 查看错误日志
2. 检查原始 HTML 格式是否正确
3. 尝试手动转换：使用 `tools/examples/` 中的工具
4. 在 WizNote 客户端中重新导出
5. 提交 Issue 寻求帮助

### Q8: 支持哪些 WizNote 版本？

**A:**
- 支持所有使用标准 API 的 WizNote 版本
- 个人版和企业版都支持
- 如果使用企业版，可能需要修改服务器地址

### Q9: 迁移后如何保持同步？

**A:** 本工具主要用于一次性迁移：
- 迁移后建议在 Obsidian 中继续使用
- 可以使用 `sync_deletions.py` 同步删除操作
- 不支持双向同步（WizNote ↔ Obsidian）

### Q10: 如何自定义配置？

**A:** 三种方式：
1. **环境变量**（推荐）：设置 `WIZNOTE_*` 环境变量
2. **配置文件**：复制 `config.example.json` 为 `config.json` 并编辑
3. **默认路径**：使用工具的默认路径设置

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

**报告问题时请提供：**
- Python 版本
- 操作系统
- 错误信息或日志
- 复现步骤
- 预期行为和实际行为

---

## 📜 开源协议

本项目采用 [MIT License](LICENSE) 开源许可证。

---

## 📚 相关文档

- [贡献指南](CONTRIBUTING.md) - 如何贡献代码
- [docs/](docs/) - 详细文档目录
  - [项目完整报告](docs/项目完整报告.md)
  - [P0 快速修复指南](docs/P0_QUICK_FIX_GUIDE.md)
  - [自动化流程分析](docs/自动化流程分析.md)

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
