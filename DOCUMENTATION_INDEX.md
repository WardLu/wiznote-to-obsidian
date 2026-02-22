# 项目文档索引

**最后更新**: 2026-02-22
**项目状态**: v1.0.0 生产就绪

---

## 📚 文档结构

```
WizNote to Obsidian/
├── README.md                              # 项目说明
├── CHANGELOG.md                           # 更新日志
├── SESSION_ANALYSIS.md                    # 会话状态分析
│
├── app/
│   ├── tasks.md                          # 任务进度跟踪
│   │
│   ├── plans/                            # 设计文档
│   │   ├── mvp-roadmap.md               # MVP 路线图
│   │   ├── 2026-02-16-desktop-app-design.md  # 桌面应用设计
│   │   ├── 2026-02-21-git-submodule-architecture.md  # Submodule 架构
│   │   └── design-review.md             # 设计评审
│   │
│   └── docs/                             # 技术文档
│       ├── DEPLOYMENT_GUIDE.md           # 部署指南
│       ├── BUILD_GUIDE.md                # 打包指南
│       ├── QUICK_START_PRODUCTION.md     # 快速开始
│       ├── ANTI_CRACK_GUIDE.md           # 防作弊指南
│       ├── VERIFICATION_GUIDE.md         # 验证指南
│       ├── SECURITY_ENHANCEMENT_REPORT.md  # 安全增强报告
│       ├── TEST_COVERAGE_REPORT.md       # 测试覆盖报告
│       ├── TEST_SUITE_COMPLETION_REPORT.md  # 测试完成报告
│       ├── ACTIVATION_404_FIX.md         # 故障排查
│       ├── LICENSE_VALIDATION_FIX.md     # 授权验证修复
│       ├── LICENSE_SYSTEM_GUIDE.md       # 授权系统指南
│       └── LICENSE_QUICK_REF.md          # 快速参考
```

---

## 🎯 按场景查找文档

### 我想快速开始

- **新用户**: `app/docs/QUICK_START_PRODUCTION.md`
- **测试授权码**: `app/docs/LICENSE_QUICK_REF.md`
- **生成授权码**: `app/tools/generate_license.py`

### 我想部署应用

- **部署服务器**: `app/docs/DEPLOYMENT_GUIDE.md`
- **打包应用**: `app/docs/BUILD_GUIDE.md`
- **运行测试**: `app/scripts/run_tests.sh`

### 我想了解技术细节

- **架构设计**: `app/plans/2026-02-16-desktop-app-design.md`
- **MVP 路线图**: `app/plans/mvp-roadmap.md`
- **Submodule 架构**: `app/plans/2026-02-21-git-submodule-architecture.md`

### 我想了解防护方案

- **防作弊详细方案**: `app/docs/ANTI_CRACK_GUIDE.md`
- **授权验证指南**: `app/docs/VERIFICATION_GUIDE.md`
- **安全增强报告**: `app/docs/SECURITY_ENHANCEMENT_REPORT.md`

### 我想了解测试

- **测试覆盖报告**: `app/docs/TEST_COVERAGE_REPORT.md`
- **测试完成报告**: `app/docs/TEST_SUITE_COMPLETION_REPORT.md`

### 我遇到了问题

- **激活 404 错误**: `app/docs/ACTIVATION_404_FIX.md`
- **授权验证问题**: `app/docs/LICENSE_VALIDATION_FIX.md`
- **授权系统指南**: `app/docs/LICENSE_SYSTEM_GUIDE.md`

### 我想查看进度

- **任务跟踪**: `app/tasks.md`
- **更新日志**: `CHANGELOG.md`
- **会话分析**: `SESSION_ANALYSIS.md`

---

## 📊 文档统计

| 类别 | 数量 | 说明 |
|------|------|------|
| **设计文档** | 4 个 | 架构设计、路线图等 |
| **技术文档** | 12 个 | 部署、测试、防护等 |
| **工具文档** | 7 个 | 脚本和工具 |
| **总计** | 23+ 个 | 完整文档体系 |

---

## 🔗 快速链接

### 主要文档

1. [README.md](../README.md) - 项目说明
2. [CHANGELOG.md](../CHANGELOG.md) - 更新日志
3. [app/tasks.md](app/tasks.md) - 任务进度
4. [app/plans/mvp-roadmap.md](app/plans/mvp-roadmap.md) - MVP 路线图

### 部署和运维

1. [DEPLOYMENT_GUIDE.md](app/docs/DEPLOYMENT_GUIDE.md) - 完整部署指南
2. [BUILD_GUIDE.md](app/docs/BUILD_GUIDE.md) - 打包指南
3. [QUICK_START_PRODUCTION.md](app/docs/QUICK_START_PRODUCTION.md) - 快速开始

### 安全和防护

1. [ANTI_CRACK_GUIDE.md](app/docs/ANTI_CRACK_GUIDE.md) - 防作弊指南
2. [SECURITY_ENHANCEMENT_REPORT.md](app/docs/SECURITY_ENHANCEMENT_REPORT.md) - 安全增强报告
3. [VERIFICATION_GUIDE.md](app/docs/VERIFICATION_GUIDE.md) - 验证指南

### 测试

1. [TEST_COVERAGE_REPORT.md](app/docs/TEST_COVERAGE_REPORT.md) - 测试覆盖报告
2. [TEST_SUITE_COMPLETION_REPORT.md](app/docs/TEST_SUITE_COMPLETION_REPORT.md) - 测试完成报告

### 故障排查

1. [ACTIVATION_404_FIX.md](app/docs/ACTIVATION_404_FIX.md) - 激活 404 修复
2. [LICENSE_VALIDATION_FIX.md](app/docs/LICENSE_VALIDATION_FIX.md) - 授权验证修复

---

## 📝 文档维护

### 更新频率

- **tasks.md**: 每次重大里程碑更新
- **CHANGELOG.md**: 每次版本发布更新
- **技术文档**: 随代码变更更新

### 归档策略

- 过期文档移动到 `docs/archive/`
- 保留最新版本的文档
- 记录文档变更历史

---

## 🆘 找不到文档？

### 检查清单

1. ✅ 检查 `app/plans/` 目录（设计文档）
2. ✅ 检查 `app/docs/` 目录（技术文档）
3. ✅ 检查根目录（README、CHANGELOG）
4. ✅ 使用 `find . -name "*关键词*"` 搜索

### 联系支持

- GitHub Issues: https://github.com/WardLu/shadow-shift/issues
- 邮箱: support@shadow.wang

---

**记住**: 所有设计文档和技术文档都在 `app/` 目录下！
