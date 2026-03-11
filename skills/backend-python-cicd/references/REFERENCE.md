# GitLab CI + Docker 流水线规范参考

## 构建与部署的两种方式（顺序：先本地，再流水线）

- **先：本地 Docker 构建测试**（**必须优先**）：在项目根目录执行多阶段构建（如 `docker build --target requirement -t ...`、`docker build --target project -t ...`），本地验证镜像能构建并可选 `docker run` 做功能验证；无需推送代码。**确认本地构建与运行无误后**，再推送代码触发流水线，避免错误提交占用 Runner 与部署环境。
- **再：Git 提交触发流水线**：对 `develop`、`bugfix/*`、`hotfix/*`、`master` 执行 `git push` 后，GitLab 根据 `.gitlab-ci.yml` **自动**创建并执行流水线（构建 → 推送镜像 → 部署），无需在 GitLab 界面手动运行。合并到上述分支后推送也会以目标分支的提交触发流水线。

## 项目仓库地址

- **默认**：**git.tac.hillstonenet.com**。克隆地址：`https://git.tac.hillstonenet.com/<组名>/<项目名>.git` 或 `git@git.tac.hillstonenet.com:<组名>/<项目名>.git`。

## 前置：远程仓库检查

使用「Git 提交触发流水线」前，需确认项目已配置指向 **git.tac.hillstonenet.com** 的远程仓库：

- 执行 `git remote -v` 检查是否已有 `origin` 且地址包含 `git.tac.hillstonenet.com`。
- **若未配置或地址不符**：提示执行 `git remote add origin https://git.tac.hillstonenet.com/<组名>/<项目名>.git` 或 `git remote set-url origin <正确地址>`，并说明「只有推送到该远程的 develop / bugfix / hotfix / master 分支后，流水线才会自动触发」。

## Git 操作说明（详细、可自动执行）

各分支场景的 Git 操作需以**可直接复制执行的命令块**或**可执行脚本**形式提供，便于用户或脚本自动执行。详见 [assets/git-operations.md](../assets/git-operations.md)，包含：检查/配置远程、克隆、日常 develop 提交、bugfix 创建/推送/合并回 develop、hotfix 创建/推送/合并回 master 与 develop、develop 合并到 master 发布生产；每段为完整命令序列，复制即用。

## 阶段与 Job

| 阶段   | Job           | 触发分支              | 说明 |
|--------|---------------|------------------------|------|
| build  | build_env     | develop                | 仅当 Dockerfile / pyproject.toml / uv.lock 任一变更时执行；构建依赖阶段镜像（--target requirement），打标签推送，供后续复用 |
| build  | build_project | develop、bugfix/*      | 构建应用镜像（--target project）；依赖未变更时复用 build_env 缓存 |
| deploy | push_image    | develop、bugfix/*、hotfix/* | 打标签并推送到私有镜像仓库 |
| deploy | dev_deploy    | develop、bugfix/*、hotfix/* | **K8s 部署**：执行 scripts/dev_deploy.sh，dev 集群 context、ConfigMap、envsubst 模板、kubectl apply、rollout restart |
| deploy | prod_deploy   | master                 | **K8s 部署**：执行 scripts/prod_deploy.sh，prod 集群；不跑 build |

## 分支约定

| 分支      | 用途           | 流水线行为 | 合并方向 |
|-----------|----------------|------------|----------|
| develop   | 主开发分支     | 推送即触发 build（依赖变更时先 build_env）→ build_project → push_image → dev_deploy | 接受 bugfix/*、hotfix/* |
| bugfix/*  | 从 develop 拉取，缺陷修复 | build_project → push_image → dev_deploy | 合并回 develop |
| hotfix/*  | 从 master 拉取，紧急修复 | 不跑 build，仅 push_image → dev_deploy；需自行保障镜像已构建 | 合并回 master 与 develop |
| master    | 生产就绪       | 仅 prod_deploy         | 接受 develop、hotfix/* |

## Docker 多阶段构建

- **依赖文件检查（必须）**：生成或校验 Dockerfile **之前**须确认项目根目录已存在依赖文件；否则 `uv sync` / `pip install` 会失败。使用 uv 时须有 `pyproject.toml` 与 `uv.lock`（缺一则 uv 安装不了）；使用 pip 时须有 `requirements.txt`。缺文件时应先提示用户创建（如 `uv init`、`uv lock`），再生成 Dockerfile。详见 [assets/dockerfile-python-base.md](../assets/dockerfile-python-base.md)「前置：检查项目依赖文件」。
- **私有镜像源参考（必须，尤其 Python）**：生成或校验 Dockerfile 时**必须**参考 [assets/dockerfile-python-base.md](../assets/dockerfile-python-base.md)。Python 基础镜像与 pip/uv 安装源均须按该文档配置。
- **Python 基础镜像（默认）**：Python 项目 Dockerfile 的 `FROM` **必须**使用 **docker.dic.hillstonenet.com/library/python:3.12-slim**，作为 requirement 与 project 阶段的基镜像，保证构建与运行环境一致且走私有镜像源；pip/uv 安装依赖须使用该文档规定的镜像源，禁止不指定源的 `pip install`。
| 阶段名     | 用途 | CI 使用 |
|------------|------|---------|
| requirement | 基于上述 Python 镜像安装 uv，复制 pyproject.toml、uv.lock，uv sync | build_env 使用 --target requirement 构建并推送依赖镜像 |
| project    | 在 requirement 基础上复制应用代码、启动脚本 | build_project 使用 --target project 构建最终镜像 |

## .gitlab-ci.yml 对应关系

- **默认 Runner tags**：`default.tags: [grunner]`，所有 Job 使用带 `grunner` tag 的 GitLab Runner 执行。
- **build_env**：`only.refs: develop`，`changes: [Dockerfile, pyproject.toml, uv.lock]`
- **build_project**：`only.refs: [develop, /^bugfix\/.*/]`
- **push_image / dev_deploy**：`only.refs: [develop, /^bugfix\/.*/, /^hotfix\/.*/]`
- **prod_deploy**：`only.refs: master`

## 场景与流水线结果速查

| 场景     | 分支        | 关键操作           | 流水线 |
|----------|-------------|--------------------|--------|
| 日常开发 | develop     | git push origin develop | build（按需 build_env）→ push_image → dev_deploy |
| 缺陷修复 | bugfix/xxx  | 从 develop 拉分支，push 后合并回 develop | build_project → push_image → dev_deploy |
| 紧急修复 | hotfix/xxx  | 从 master 拉分支，合并回 master + develop | hotfix 推送：push_image → dev_deploy；master 推送：prod_deploy |
| 生产发布 | master      | 将 develop 或 hotfix 合并到 master 后 push | 仅 prod_deploy |

## 私有镜像仓库

- **推送地址**：镜像推送到私有仓库 **registry.dic.hillstonenet.com**，命名空间为 **private**；完整镜像地址形如 `registry.dic.hillstonenet.com/private/<项目名>:<标签>`（如 `registry.dic.hillstonenet.com/private/myapp:latest`）。
- **CI 内登录**：在 build_env、build_project、push_image 等需与仓库交互的 Job 中，在 `docker build`/`docker push` 前执行 `docker login registry.dic.hillstonenet.com -u $REGISTRY_USER -p $REGISTRY_PASSWORD`（或 `--password-stdin`）；用户名与密码放在 GitLab CI/CD Variables 中（可设为 Masked），不在代码或日志中明文写出。
- **镜像地址**：CI 变量建议 `PRIVATE_REGISTRY=registry.dic.hillstonenet.com`、`IMAGE_NAMESPACE=private`，拼接为 `$PRIVATE_REGISTRY/$IMAGE_NAMESPACE/$CI_PROJECT_NAME:latest`。
- **部署/运维**：在需要拉取镜像的机器上，先执行 `docker login registry.dic.hillstonenet.com`，再 `docker pull registry.dic.hillstonenet.com/private/<项目名>:latest`；文档中需写明「使用私有仓库时需先登录」及凭证管理建议。

## 部署后 Docker 运行

- **使用私有仓库时**：先 `docker login registry.dic.hillstonenet.com -u <用户> -p <密码>`，再 `docker pull registry.dic.hillstonenet.com/private/<项目名>:latest`。
- 运行：容器内应用端口（如 5000）需映射；通过环境变量区分 ENV=dev（开发模式）与 ENV=prod（Gunicorn）；SECRET_KEY、数据库、Redis 等由环境变量或 --env-file 注入。
- 更新：拉取新镜像后停止并删除旧容器，再 docker run 创建新容器。

## 部署方式：dev → prod，必须使用 K8s

- **约定**：部署**必须**为 dev（测试）→ prod（生产）两环境，且**必须**通过 Kubernetes 部署；在 `.gitlab-ci.yml` 中 dev_deploy 调用 `scripts/dev_deploy.sh`，prod_deploy 调用 `scripts/prod_deploy.sh`。
- **Dev 模板**：使用 `dev_deployment.yaml.tpl`（见 assets/k8s/dev_deployment.yaml.tpl），变量 `${CI_PROJECT_NAME}` 由 envsubst 替换；含 Deployment、Service、Ingress。命名空间 `api-server`，镜像 `docker.dic.hillstonenet.com/private/${CI_PROJECT_NAME}:latest`，ConfigMap `${CI_PROJECT_NAME}-env`，imagePullSecrets `docker-registry`，dnsPolicy None + 指定 nameservers；Ingress host `${CI_PROJECT_NAME}.apistest.dic.hillstonenet.com`，ingressClassName `api-server`。
- **dev_deploy.sh 流程**：`kubectl config use-context kubernetes-admin-dev@kubernetes`；若 .env.example 无 `ENV=dev` 则 prepend；若 ConfigMap `${CI_PROJECT_NAME}-env` 不存在则 `kubectl create configmap ... --from-env-file=.env.example -n api-server`；`envsubst < dev_deployment.yaml.tpl > deployment.yaml`（模板路径可为项目内 `k8s/dev_deployment.yaml.tpl` 或 Runner 固定路径如 `/.flaskserver/dev_deployment.yaml.tpl`）；`kubectl apply -f deployment.yaml`；`kubectl rollout restart deployment ${CI_PROJECT_NAME} -n api-server`。
- **prod_deploy.sh**：切换 context 到 prod（如 `kubernetes-admin-prod@kubernetes`），ENV=prod，可选 prod 专用模板（如不同 Ingress host）；其余同 dev。
- **前置**：命名空间 api-server、Secret docker-registry 需已在集群中存在；ConfigMap 可由脚本在首次部署时从 .env.example 创建。
