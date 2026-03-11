# Docker 多阶段构建命令（与 CI 一致）

**请先使用本地 Docker 构建与测试，再通过 Git 推送触发流水线。**

本页命令用于**本地 Docker 构建与测试**，无需推送代码即可验证镜像能否正常构建与运行；建议在每次修改 Dockerfile、依赖或应用代码后**先执行本地构建并验证通过**，再执行 `git push`。若跳过本地验证直接推送，可能触发失败的流水线并占用 Runner 与部署环境。通过 Git 提交触发流水线前，需确保项目已配置 GitLab 远程仓库（`git remote -v`），再推送到 develop / bugfix / hotfix / master 分支。

## 与 CI 对应的本地构建

```bash
# 1. 先构建依赖阶段并打标签（与 CI 中 build_env 一致）
docker build --target requirement -t <镜像仓库>/<项目名>:requirement .

# 2. 再构建应用阶段（会复用上一阶段）
docker build --target project -t <镜像仓库>/<项目名>:latest .
```

## 说明

- **Python 基础镜像**：默认使用 `docker.dic.hillstonenet.com/library/python:3.12-slim`（Dockerfile 中 `FROM docker.dic.hillstonenet.com/library/python:3.12-slim`）。
- `requirement` 阶段：在上述镜像上安装 uv，复制 pyproject.toml、uv.lock 并执行 uv sync，产出仅含依赖的中间镜像。
- `project` 阶段：在 requirement 基础上复制应用代码、设置启动命令，产出可运行的应用镜像。
- CI 中 build_env 推送的 requirement 镜像可供 build_project 复用，减少重复 uv sync。
