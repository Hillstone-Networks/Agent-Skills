# 流水线概览

## 阶段与 Job（与 REFERENCE 一致）

| 阶段 | Job | 触发分支 | 触发条件 / 说明 |
|------|-----|----------|------------------|
| build | build_env | develop | 仅当 Dockerfile、pyproject.toml、uv.lock 任一变更时执行；构建依赖镜像（requirement 阶段） |
| build | build_project | develop、bugfix/* | 构建应用镜像（project 目标）；依赖未变更时复用 build_env 缓存 |
| deploy | push_image | develop、bugfix/*、hotfix/* | 打标签并推送到私有镜像仓库 |
| deploy | dev_deploy | develop、bugfix/*、hotfix/* | 执行开发环境部署脚本 |
| deploy | prod_deploy | master | 仅 master 触发；执行生产环境部署脚本 |

## 约定要点

- 依赖镜像仅 develop 在依赖文件变更时构建（build_env）；bugfix/* 不单独构建依赖镜像。
- 开发/生产隔离：推镜像 + 开发部署由 develop、bugfix/*、hotfix/* 触发；生产部署仅由 master 触发。
- hotfix/* 不触发 build_env、build_project，仅 push_image、dev_deploy；需确保镜像已通过 develop 等构建。
