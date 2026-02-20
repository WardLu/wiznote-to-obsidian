# 项目架构说明

> **更新日期**: 2026-02-21
> **架构方案**: Git Submodule

---

## 📋 架构概述

本项目采用 **开源工具 + 商业应用** 的双轨架构：

- **开源部分**：命令行工具，免费供社区使用
- **商业部分**：桌面应用，提供图形界面和授权管理

---

## 🏗️ 架构设计

```
公开仓库 (wiznote-to-obsidian)
│
├── tools/                    # 开源命令行工具 ✅
│   ├── wiznote_downloader.py # 下载工具
│   ├── obsidian_formatter.py # 格式化工具
│   └── ...                   # 其他工具
│
├── app/ → shadow-shift       # 商业应用 Submodule 🔒
│
└── 文档                       # 开源项目文档
```

### 为什么这样设计？

1. **开源初衷**：希望迁移工具免费开源，帮助社区用户
2. **商业需求**：桌面应用提供更好的用户体验，需要商业化支持
3. **代码复用**：商业应用可以复用开源工具的能力
4. **版本管理**：可以锁定特定版本的开源工具

---

## 📂 仓库说明

### 公开仓库（本仓库）

- **地址**: https://github.com/WardLu/wiznote-to-obsidian
- **可见性**: Public
- **内容**:
  - `tools/` - 开源命令行工具
  - `README.md` - 使用文档
  - `CHANGELOG.md` - 更新日志
  - `SUBMODULE_SETUP.md` - Submodule 操作指南

**适用人群**:
- ✅ 所有用户都可以使用
- ✅ 完全免费开源（MIT License）

---

### 私有仓库（shadow-shift）

- **地址**: https://github.com/WardLu/shadow-shift (Private)
- **可见性**: Private
- **内容**:
  - `src/` - 桌面应用源码
  - `server/` - Serverless API
  - `tests/` - 测试代码
  - `plans/` - 设计文档

**适用人群**:
- ✅ 项目维护者
- ✅ 付费用户（未来可能开放部分访问）

---

## 📖 Submodule 使用指南

### 对于开源用户

如果你只想使用开源工具，**不需要**关心 `app/` 目录：

```bash
# 只 clone 公开仓库
git clone https://github.com/WardLu/wiznote-to-obsidian.git
cd wiznote-to-obsidian

# 直接使用工具
python3 tools/wiznote_downloader.py
python3 tools/obsidian_formatter.py
```

**注意**: `app/` 目录会是空的，这是正常的，不影响开源工具的使用。

---

### 对于项目维护者

如果你需要访问完整的商业应用代码：

```bash
# 递归 clone（包含 submodule）
git clone --recursive git@github.com:WardLu/wiznote-to-obsidian.git

# 或分步 clone
git clone git@github.com:WardLu/wiznote-to-obsidian.git
cd wiznote-to-obsidian
git submodule init
git submodule update
```

**前提**: 需要有私有仓库 `shadow-shift` 的访问权限。

---

## 🔒 安全说明

### 访问权限

| 目录 | 开源用户 | 维护者 |
|-----|---------|-------|
| `tools/` | ✅ 完全访问 | ✅ 完全访问 |
| `app/` | ❌ 目录为空 | ✅ 完整代码 |
| 私有仓库 | ❌ 无法访问 | ✅ 完全访问 |

### Submodule 配置

我们使用 **相对路径** 配置 submodule，保护私有仓库地址：

```ini
[submodule "app"]
    path = app
    url = ../shadow-shift.git  # 相对路径，不暴露完整 URL
```

---

## 📚 相关文档

### 公开文档（本仓库）

- **[README.md](README.md)** - 开源工具使用指南
- **[SUBMODULE_SETUP.md](SUBMODULE_SETUP.md)** - Submodule 详细操作指南
- **[CHANGELOG.md](CHANGELOG.md)** - 项目更新日志

### 私有文档（需要权限）

以下文档存储在私有仓库，需要访问权限：

- **架构设计文档** - 完整的架构设计、方案对比、实施记录
- **任务进度跟踪** - 项目开发进度、下一步计划
- **桌面应用设计** - GUI 设计、授权系统、打包配置
- **MVP 路线图** - 产品迭代计划

---

## 🤝 贡献指南

### 贡献开源工具

如果你想改进开源工具：

1. Fork 本仓库
2. 修改 `tools/` 目录下的代码
3. 提交 Pull Request

参考: [CONTRIBUTING.md](CONTRIBUTING.md)

---

### 商业合作

如果你对商业应用感兴趣：

- 购买授权：访问 [私有仓库](https://github.com/WardLu/shadow-shift) 了解更多信息
- 技术支持：通过 GitHub Issues 联系

---

## ❓ 常见问题

### Q1: 我能使用商业应用吗？

**A**: 商业应用需要购买授权。开源工具完全免费，你可以先用开源工具体验功能。

---

### Q2: app/ 目录为什么是空的？

**A**: `app/` 是一个 Git Submodule，指向私有仓库。如果你没有私有仓库权限，这个目录会是空的，这是正常的。

---

### Q3: 开源工具和商业应用有什么区别？

| 特性 | 开源工具 | 商业应用 |
|-----|---------|---------|
| **界面** | 命令行 | 图形界面 |
| **价格** | 免费 | 付费 |
| **授权** | MIT | 商业授权 |
| **支持** | 社区 | 官方支持 |
| **功能** | 完整功能 | 完整功能 + 授权管理 |

---

### Q4: 如何选择？

**建议**:

- ✅ **技术用户**：使用开源工具，灵活自由
- ✅ **非技术用户**：使用商业应用，图形界面更友好
- ✅ **企业用户**：购买商业授权，获得官方支持

---

## 📞 联系方式

- **GitHub Issues**: https://github.com/WardLu/wiznote-to-obsidian/issues
- **私有仓库**: https://github.com/WardLu/shadow-shift

---

## 📜 许可证

- **开源工具**: [MIT License](LICENSE)
- **商业应用**: 商业授权（私有仓库）

---

**最后更新**: 2026-02-21
