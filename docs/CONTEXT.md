# 项目上下文文档

**最后更新**: 2026-02-25 18:00
**当前版本**: v1.3.8
**项目状态**: ✅ 稳定开发中

---

## 🎯 项目概述

**项目名称**: WizNote to Obsidian 迁移工具
**项目类型**: 桌面应用（GUI）+ 命令行工具
**核心功能**: 将为知笔记迁移到 Obsidian 格式
**商业模式**: 授权码激活（¥49.00 / 1天试用）

### 技术栈
- **语言**: Python 3.12
- **GUI**: CustomTkinter (基于 Tkinter)
- **数据库**: Supabase (PostgreSQL)
- **测试**: pytest + coverage
- **打包**: PyInstaller

---

## 📊 当前状态

### ✅ 已完成功能
1. **核心迁移功能**
   - 在线下载为知笔记
   - HTML → Markdown 转换
   - 图片和附件自动下载
   - WikiLinks 链接转换
   - 语法检查和格式修复

2. **商业授权系统**
   - 授权码生成和管理
   - 在线/离线激活
   - 授权状态持久化
   - 云端同步和降级策略
   - 设备绑定和防作弊

3. **GUI 界面**
   - 登录验证
   - 实时进度显示
   - 授权激活面板
   - 购买信息展示
   - 工具按钮（格式化、附件迁移）

4. **测试体系**（v1.3.8 新增）
   - 单元测试：12 个测试
   - 集成测试：8 个测试
   - E2E 测试：5 个测试
   - 总通过率：92%

### 🚧 进行中的工作
- 暂无

### 📋 计划中的功能
1. **v1.3.9 或 v1.4.0**
   - 修复 E2E 测试失败问题
   - 提升测试覆盖率至 30%+
   - 性能测试和优化

2. **v2.0.0（未来）**
   - 插件系统
   - 国际化支持
   - 云端同步功能

---

## 🏗️ 项目结构

```
wiznote-to-obsidian/
├── app/                    # 主应用（Git Submodule）
│   ├── gui/               # GUI 界面
│   ├── server/            # 授权服务器 API
│   │   ├── api/          # API 端点
│   │   └── lib/          # 核心库
│   ├── tests/            # 测试文件
│   │   ├── unit/        # 单元测试
│   │   ├── integration/ # 集成测试
│   │   └── e2e/         # E2E 测试
│   └── tools/           # 命令行工具
├── docs/                  # 文档
│   ├── archive/          # 版本归档
│   │   └── v1.3.8/      # v1.3.8 归档文档
│   ├── plans/            # 规划文档
│   └── reports/          # 报告文档
├── tools/                 # 项目工具
└── assets/                # 资源文件
```

---

## 🔑 关键技术决策

### 1. Git Submodule 架构
- **主仓库**: 文档、工具、测试
- **子模块 (app/)**: 核心应用代码
- **原因**: 分离开源和闭源代码

### 2. 授权系统设计
- **在线优先**: 云端验证 + 离线缓存
- **降级策略**: 云端失败自动降级到缓存
- **设备绑定**: UUID 绑定，防止多设备使用
- **有效期**: 1 天试用，付费永久

### 3. 测试策略
- **测试金字塔**: 单元 → 集成 → E2E
- **Mock 策略**: Mock Supabase，真实缓存
- **覆盖率目标**: 50%+（当前 17%）

---

## 📈 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|---------|
| v1.3.8 | 2026-02-25 | 离线授权修复 + 完整测试覆盖 |
| v1.3.7 | 2026-02-24 | GUI 优化（官网链接、关于对话框） |
| v1.3.6 | 2026-02-23 | Pillow 依赖兼容性修复 |
| v1.3.5 | 2026-02-23 | 测试用例修复和新增 |
| v1.3.4 | 2026-02-23 | 打包验证和服务端验证 |
| v1.3.3 | 2026-02-23 | GUI 进度条增强 |
| v1.3.2 | 2026-02-23 | 在线检测更新功能 |
| v1.3.1 | 2026-02-23 | 购买授权弹窗二维码 |
| v1.3.0 | 2026-02-22 | 安全增强（加密存储、服务器验证、代码混淆） |
| v1.1.0 | 2026-02-16 | 协作笔记支持 |
| v1.0.0 | 2026-01-27 | 首次发布 |

**详细变更记录**: 查看 `CHANGELOG.md`

---

## 🧪 测试状态

### 当前测试覆盖

```
        E2E (5 个测试, 80% 通过)
       /              \
    集成 (8 个测试, 100% 通过)
   /                    \
单元 (12 个测试, 100% 通过)
```

- **总测试数**: 25 个
- **总通过率**: 92%（23/25）
- **代码覆盖率**: 17%

### 已测试的功能
- ✅ 离线激活和验证
- ✅ 授权状态持久化
- ✅ 降级策略
- ✅ 重复激活处理
- ✅ 设备绑定验证

### 未测试的功能
- ⚠️ GUI 界面交互
- ⚠️ 下载和迁移流程
- ⚠️ 性能和并发
- ⚠️ 错误处理边界情况

---

## ⚠️ 已知问题

### 高优先级
- 暂无

### 中优先级
1. **E2E 测试失败**（v1.3.8）
   - 测试: `test_reactivation_shows_renewal_message`
   - 通过率: 80%（4/5）
   - 影响: 核心功能正常，仅测试逻辑问题

### 低优先级
1. **测试覆盖率低**
   - 当前: 17%
   - 目标: 50%+

---

## 🔄 开发流程

### Git 工作流
- **主分支**: `main`
- **提交规范**: Conventional Commits
- **子模块**: 独立版本控制

### 提交消息格式
```
<type>(<scope>): <subject>

<body>

Generated with [Claude Code](https://claude.ai/code)
via [Happy](https://happy.engineering)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: Happy <yesreply@happy.engineering>
```

### 常用命令
```bash
# 运行测试
cd app
pytest tests/

# 运行特定测试
pytest tests/unit/test_offline_activation.py -v

# 查看覆盖率
pytest --cov=server tests/

# 更新子模块
git submodule update --remote

# 提交子模块变更
cd app
git add .
git commit -m "xxx"
git push
cd ..
git add app
git commit -m "chore: 更新 app submodule - xxx"
```

---

## 📚 重要文档

### 开发文档
- `CHANGELOG.md` - 版本更新日志
- `README.md` - 项目说明
- `docs/archive/v1.3.8/VERSION_SUMMARY.md` - v1.3.8 版本总结

### 规划文档
- `docs/plans/2026-02-25-offline-auth-tests-plan.md` - 单元测试计划
- `docs/plans/2026-02-25-offline-integration-tests-plan.md` - 集成测试计划

### 报告文档
- `docs/reports/README.md` - 报告索引
- `docs/reports/RELEASE_v1.3.0.md` - v1.3.0 发布报告

---

## 🔧 环境配置

### 开发环境
- Python: 3.12
- 操作系统: macOS (开发), Windows/Linux (支持)
- 依赖管理: pip + requirements.txt

### 关键依赖
- `customtkinter` - GUI 框架
- `requests` - HTTP 请求
- `markdownify` - HTML 转 Markdown
- `supabase` - 数据库客户端
- `pytest` - 测试框架
- `freezegun` - 时间测试工具

### 环境变量（.env）
```
SUPABASE_URL=<url>
SUPABASE_KEY=<key>
```

---

## 🎯 下一步行动

### 立即行动
- 暂无紧急任务

### 短期计划（1-2 周）
1. 修复 E2E 测试失败问题
2. 继续提升测试覆盖率
3. 优化离线模式性能

### 长期计划（1-3 个月）
1. 达到 50%+ 测试覆盖率
2. 添加性能测试
3. 探索国际化支持

---

## 📞 联系方式

- **官网**: https://shadow.wang
- **邮箱**: shadow@shadow.wang
- **微信**: 见 `assets/wechat_contact.png`

---

**文档维护**: 每次重要更新后维护此文档
**下次更新**: v1.3.9 或 v1.4.0 发布时
