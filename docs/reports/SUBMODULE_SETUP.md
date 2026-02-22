# Git Submodule 设置指南

## 📋 当前状态

### ✅ 已完成

1. **私有仓库初始化**
   - 位置: `/Users/wardlu/Documents/VibeCoding/Wiznot to obisidian App`
   - Git 已初始化并提交（102 个文件）
   - 包含所有商业代码：`src/`, `server/`, `tests/`, `api/` 等

2. **公开仓库配置**
   - 添加了 `.gitmodules` 配置
   - submodule 路径: `app/`
   - 使用相对路径: `../wiznote2obsidian-app.git`

3. **代码清理**
   - 公开仓库已删除所有商业代码
   - 保持干净的开源项目结构

---

## 🚀 下一步操作

### 步骤 1: 在 GitHub 创建私有仓库

1. 访问 https://github.com/new
2. 仓库设置:
   - **Repository name**: `wiznote2obsidian-app`
   - **Description**: `WizNote to Obsidian Desktop App (Commercial)`
   - **Visibility**: ✅ Private
   - **不要**勾选 "Add a README file"
   - **不要**勾选 "Add .gitignore"
3. 点击 "Create repository"

### 步骤 2: 推送私有仓库

```bash
cd "/Users/wardlu/Documents/VibeCoding/Wiznot to obisidian App"

# 添加远程仓库
git remote add origin git@github.com:WardLu/wiznote2obsidian-app.git

# 推送到 GitHub
git push -u origin main
```

### 步骤 3: 在公开仓库初始化 Submodule

```bash
cd "/Users/wardlu/Documents/VibeCoding/Wiznote to Obisidian"

# 初始化 submodule（会创建 app/ 目录）
git submodule add git@github.com:WardLu/wiznote2obsidian-app.git app

# 提交 submodule 配置
git add .gitmodules app/
git commit -m "feat: 添加商业化应用 submodule"
```

### 步骤 4: 验证 Submodule

```bash
# 检查 submodule 状态
git submodule status

# 应该看到类似输出：
# <commit-hash> app (heads/main)
```

---

## 📖 日常开发流程

### 更新私有仓库代码

```bash
# 在私有仓库修改代码
cd "/Users/wardlu/Documents/VibeCoding/Wiznot to obisidian App"
vim src/main.py

# 提交并推送
git add .
git commit -m "feat: 新功能"
git push
```

### 在公开仓库同步 Submodule 引用

```bash
cd "/Users/wardlu/Documents/VibeCoding/Wiznote to Obisidian"

# 更新 submodule 到最新版本
git submodule update --remote app

# 提交 submodule 版本更新
git add app/
git commit -m "chore: 更新 app submodule 到最新版本"
git push
```

### Clone 包含 Submodule 的项目

```bash
# 方式 1: 递归 clone（推荐）
git clone --recursive git@github.com:WardLu/wiznote-to-obsidian.git

# 方式 2: 先 clone 再初始化
git clone git@github.com:WardLu/wiznote-to-obsidian.git
cd wiznote-to-obsidian
git submodule init
git submodule update
```

---

## 🔒 安全说明

### 为什么使用相对路径？

`.gitmodules` 中使用 `../wiznote2obsidian-app.git` 而不是完整 URL：

```ini
# ✅ 推荐：相对路径（隐藏私有仓库地址）
url = ../wiznote2obsidian-app.git

# ❌ 不推荐：完整路径（暴露私有仓库地址）
url = git@github.com:WardLu/wiznote2obsidian-app.git
```

**好处**：
1. 不暴露私有仓库名称
2. 即使有人访问公开仓库，也无法知道私有仓库的确切地址
3. 需要权限才能访问 submodule

### 访问控制

- ✅ 公开仓库所有人可见
- ✅ 私有仓库只有你可见（Private）
- ✅ Clone 时会自动验证权限：
  - 有权限 → 成功 clone submodule
  - 无权限 → submodule 目录为空（不影响公开仓库使用）

---

## ⚠️ 常见问题

### Q1: 如何在不访问私有仓库的情况下使用开源工具？

**A**: 私有 submodule 不会影响开源工具的使用：

```bash
# 只 clone 公开仓库
git clone git@github.com:WardLu/wiznote-to-obsidian.git

# 可以正常使用 tools/ 目录下的所有工具
python3 tools/wiznote_downloader.py
python3 tools/obsidian_formatter.py
```

### Q2: 如何删除 submodule？

**A**: 按顺序执行：

```bash
# 1. 取消注册 submodule
git submodule deinit -f app/

# 2. 删除 submodule 目录
rm -rf .git/modules/app

# 3. 删除 submodule 配置
git rm -f app/

# 4. 删除 .gitmodules
rm .gitmodules

# 5. 提交更改
git commit -m "chore: 移除 app submodule"
```

### Q3: Submodule 更新后如何同步？

**A**:

```bash
# 在公开仓库更新到最新版本
git submodule update --remote app

# 或更新所有 submodule
git submodule update --remote
```

---

## 📊 架构图

```
GitHub
├── wiznote-to-obsidian (Public)
│   ├── tools/                # 开源命令行工具
│   ├── README.md
│   ├── .gitmodules           # submodule 配置
│   └── app/ -> wiznote2obsidian-app (Submodule 引用)
│       ├── src/              # 桌面应用源码
│       ├── server/           # Serverless API
│       └── tests/            # 测试
│
└── wiznote2obsidian-app (Private)
    ├── src/                  # 桌面应用源码（实际代码）
    ├── server/               # Serverless API（实际代码）
    └── tests/                # 测试（实际代码）
```

---

## ✅ 检查清单

完成设置后，请验证：

- [ ] GitHub 私有仓库已创建
- [ ] 私有仓库代码已推送
- [ ] 公开仓库 submodule 已初始化
- [ ] `git submodule status` 显示正常
- [ ] `app/` 目录包含所有商业代码
- [ ] `.gitignore` 包含 `app/`

---

## 📚 参考资料

- [Git Submodule 官方文档](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [GitHub Submodule 最佳实践](https://docs.github.com/en/repositories/working-with-files/managing-files/using-submodules)

---

**文档版本**: 1.0.0
**最后更新**: 2026-02-20
