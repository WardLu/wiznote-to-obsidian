# 更新日志

本文档记录 WizNote to Obsidian 项目的所有重要更改。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.2.0] - 2026-02-22

### 新增功能

#### 商业应用 (app/)

- ✅ **登录验证** - 在迁移前验证为知笔记账号密码
  - 返回详细错误信息（如"用户名或密码错误"）
  - 登录失败弹窗提示用户
  - 阻止后续迁移流程

- ✅ **单实例检查** - 使用文件锁防止重复打开应用
  - 同一时间只能运行一个实例
  - 友好的错误提示
  - 退出时自动清理锁文件

- ✅ **实时进度更新** - GUI 进度条实时显示
  - 进度条实时更新百分比
  - 进度文本显示：`下载中 X/Y (Z%)`
  - `WizMigrator` 支持 `on_progress` 回调

- ✅ **实时日志显示** - 迁移日志同时输出到命令行和 GUI
  - GUI 操作日志区域实时滚动显示
  - 方便调试和用户查看

- ✅ **依赖检查** - 启动时自动检查依赖项
  - 必需依赖：customtkinter, markdownify, requests
  - 可选依赖：websocket-client（协作笔记功能）
  - 缺少依赖时显示安装命令

- ✅ **启动脚本** - 简化启动流程
  - `start.sh` - 项目根目录便捷启动
  - `run_gui.sh` - 自动检查依赖，使用 Homebrew Python

#### UI/UX 改进

- 🎨 **恢复苹果极简风格** - 深色背景 `#1a1a2e`，圆角卡片设计
- 🎨 **渐变色按钮** - 更现代的视觉效果
- 🎨 **紧凑布局** - 优化间距和排版

### Bug 修复

- 🐛 修复 GUI 启动崩溃（使用 Homebrew Python 避免系统 Tk 兼容性问题）
- 🐛 修复 signal 错误（移除主线程限制的 signal 超时机制）
- 🐛 修复日志不显示（同时输出到命令行和 GUI）

### 开源工具改进

- 🔧 **WizMigrator.login()** 返回 `(success, error_message)` 元组
- 🔧 **WizMigrator.__init__()** 添加 `on_progress` 回调参数
- 🔧 每个笔记下载完成后调用进度回调

### 文档更新

- 📝 **ARCHITECTURE.md** - Git Submodule 架构说明
- 📝 **COMMIT_REPORT.md** - 详细的提交记录和测试报告
- 📝 **app/CHANGELOG.md** - 子模块更新日志

### 项目结构优化

- 🧹 清理测试文件
- 🧹 删除重复的项目副本
- 🧹 整理目录结构

### 统计信息

- 主仓库提交：11 个
- 子模块提交：9 个
- 修改文件：5 个核心文件
- 新增文件：3 个文档文件

## [1.1.0] - 2026-02-16

### 新增功能

- ✅ **协作笔记支持** - 通过 ShareJS 协议自动获取协作笔记内容
  - 实现完整的 WebSocket 握手协议（3次 hs + 认证）
  - 自动获取协作笔记内容（fetch + 双次接收）
  - 转换 ShareJS 格式为标准 Markdown
  - 支持所有 block 类型（text、list、code、table、embed）
  - 支持评论系统、数学公式、流程图等高级功能

- ✅ **协作笔记解析器** (`tools/collaboration_note_parser.py`)
  - 450+ 行完整实现
  - 策略模式处理不同的 block 类型
  - 完整的 Markdown 转换支持

- ✅ **附件集中管理** - `--all` 参数可选执行附件迁移
  - 附件复制到 `attachments/` 目录
  - 自动添加附件链接

- ✅ **安全输出目录** - 格式化输出到 `wiznote_obsidian/`
  - 原始 `wiznote_download/` 保持不变
  - 避免修改源数据

### 性能提升

- ⚡ 协作笔记成功率：0% → 100%（25/25）
- ⚡ 总体成功率：94% → 99.6%（447/449）
- ⚡ 并发下载：3 线程，2分20秒完成 449 个笔记

### 改进

- 🔧 修复登录逻辑（支持两种 returnCode 格式）
- 🔧 添加 user_guid 保存（WebSocket 认证需要）
- 🔧 优化 Markdown 处理（协作笔记直接保存）
- 🔧 改进错误提示和调试输出
- 🔧 简化命令：默认执行基础5步，`--all` 执行完整7步

### 文档更新

- 📝 整合所有文档到 README.md
- 📝 更新工具说明
- 📝 添加使用场景和常见问题

### 实际测试结果

```
测试环境：真实 WizNote 账号
笔记总数：449 个
成功下载：447 个（99.6%）
图片：7198 张（100%）
附件：30 个（100%）
协作笔记：25 个（100%）
总耗时：2 分 20 秒
```

### 参考实现

感谢 [awaken233/wiz2obsidian](https://github.com/awaken233/wiz2obsidian) 项目提供的 ShareJS 协议参考实现。

---

## [1.0.0] - 2026-01-27

### 首次发布

- ✅ 在线下载工具（`wiznote_downloader.py`）
- ✅ 离线格式化工具（`obsidian_formatter.py`）
- ✅ HTML → Markdown 转换
- ✅ 图片自动下载
- ✅ 附件自动下载
- ✅ WikiLinks 链接转换
- ✅ 语法检查和格式修复
- ✅ 同步删除工具
- ✅ 附件迁移工具
