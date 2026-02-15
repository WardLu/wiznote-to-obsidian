# 更新日志

本文档记录 WizNote to Obsidian 项目的所有重要更改。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

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
