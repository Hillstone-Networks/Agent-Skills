# Git 操作说明（可自动执行）

项目仓库地址：**git.tac.hillstonenet.com**。以下命令块均可直接复制到终端顺序执行（将 `<组名>`、`<项目名>` 替换为实际值）。克隆地址格式：
- HTTPS：`https://git.tac.hillstonenet.com/<组名>/<项目名>.git`
- SSH：`git@git.tac.hillstonenet.com:<组名>/<项目名>.git`

---

## 1. 检查或配置远程仓库

```bash
# 检查当前远程
git remote -v

# 若无 origin 或地址不是 git.tac.hillstonenet.com，添加/修改为（二选一）：
# HTTPS（需输入账号密码或配置凭证）
git remote add origin https://git.tac.hillstonenet.com/<组名>/<项目名>.git
# 若已存在 origin 但地址错误：
# git remote set-url origin https://git.tac.hillstonenet.com/<组名>/<项目名>.git

# SSH（需已配置 SSH 公钥）
git remote add origin git@git.tac.hillstonenet.com:<组名>/<项目名>.git
# 若已存在 origin 但地址错误：
# git remote set-url origin git@git.tac.hillstonenet.com:<组名>/<项目名>.git
```

---

## 2. 克隆项目（首次）

```bash
# HTTPS
git clone https://git.tac.hillstonenet.com/<组名>/<项目名>.git
cd <项目名>

# 或 SSH
git clone git@git.tac.hillstonenet.com:<组名>/<项目名>.git
cd <项目名>
```

---

## 3. 日常开发（在 develop 上提交并触发开发环境流水线）

```bash
git checkout develop
git pull origin develop
# ... 修改代码 ...
git add .
git commit -m "feat: 描述改动"
git push origin develop
```

执行后 GitLab 自动触发：build_project → push_image → dev_deploy。

---

## 4. 缺陷修复（从 develop 拉 bugfix 分支，推送后触发流水线，再合并回 develop）

```bash
# 创建并推送 bugfix 分支
git checkout develop
git pull origin develop
git checkout -b bugfix/问题简述
# ... 修改代码 ...
git add .
git commit -m "fix: 描述修复"
git push origin bugfix/问题简述
```

流水线触发：build_project → push_image → dev_deploy。验证通过后合并回 develop：

```bash
git checkout develop
git pull origin develop
git merge bugfix/问题简述
git push origin develop
```

---

## 5. 紧急热修（从 master 拉 hotfix，推送后仅部署不构建，再合并回 master 与 develop）

```bash
# 创建并推送 hotfix 分支
git checkout master
git pull origin master
git checkout -b hotfix/问题简述
# ... 修改代码 ...
git add .
git commit -m "hotfix: 描述紧急修复"
git push origin hotfix/问题简述
```

流水线触发：push_image → dev_deploy（不构建新镜像）。合并回 master 触发生产部署：

```bash
git checkout master
git pull origin master
git merge hotfix/问题简述
git push origin master
```

同步到 develop：

```bash
git checkout develop
git pull origin develop
git merge hotfix/问题简述
git push origin develop
```

---

## 6. 发布到生产（将 develop 合并到 master 并推送）

```bash
git checkout develop
git pull origin develop
git checkout master
git pull origin master
git merge develop
git push origin master
```

执行后仅触发 prod_deploy，不重新构建镜像。

---

## 7. 一键检查远程并提示（可放入脚本或文档）

```bash
if ! git remote get-url origin 2>/dev/null | grep -q 'git.tac.hillstonenet.com'; then
  echo "未配置 git.tac.hillstonenet.com 远程仓库，请执行："
  echo "  git remote add origin https://git.tac.hillstonenet.com/<组名>/<项目名>.git"
  echo "或："
  echo "  git remote set-url origin https://git.tac.hillstonenet.com/<组名>/<项目名>.git"
  exit 1
fi
echo "远程仓库已配置，可执行 git push 触发流水线。"
```

生成项目文档时，可将上述各场景命令块原样放入「Git 操作说明」章节，便于用户复制执行；或提供 `scripts/git-<场景>.sh` 脚本封装上述命令（接收可选参数如分支名、commit message），实现可自动执行。
