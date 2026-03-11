---
name: backend-api-cicd
description: 根据 GitLab CI 与 Docker 多阶段构建规范，生成或校验 .gitlab-ci.yml、分支约定与部署脚本；强调先使用本地 Docker 构建测试、再通过 Git 提交触发流水线。在用户要配置 GitLab CI、Docker 流水线、分支策略或部署流程时使用。
---

# GitLab CI + Docker 流水线

按「build → deploy」两阶段、分支触发规则与 Docker 多阶段构建，生成或维护 `.gitlab-ci.yml`、分支使用说明及部署脚本。**部署方式固定为 dev → prod，且必须使用 Kubernetes（K8s）部署**；在 `.gitlab-ci.yml` 中通过 dev_deploy / prod_deploy 调用 K8s 部署脚本，使用模板（如 `dev_deployment.yaml.tpl`）经 `envsubst` 替换后 `kubectl apply`。详细约定见 [references/REFERENCE.md](references/REFERENCE.md)。

## 何时使用

- 用户要求「配置 GitLab CI」「写 .gitlab-ci.yml」「Docker 多阶段构建 + CI」「分支与部署流程」
- 用户需要流水线说明、分支约定或部署后 Docker 运行说明；或需区分「本地 Docker 构建测试」与「Git 提交触发流水线」两种方式、以及远程仓库前置检查

## 使用流程

### 0. 前置：远程仓库与构建方式

**推荐顺序：先使用本地 Docker 构建测试，再通过 Git 提交触发流水线。**

1. **先：本地 Docker 构建与测试**（**必须优先执行**）：在项目根目录执行多阶段构建（见 [assets/docker-build-commands.md](assets/docker-build-commands.md)），本地验证镜像能否正常构建与运行，并可本地 `docker run` 做接口或功能验证；无需推送代码。**在确认本地构建与运行无误后**，再执行步骤 2，避免有问题的提交触发流水线、占用 Runner 与部署环境。
2. **再：通过 Git 提交触发流水线**：将代码推送到配置了 GitLab CI 的**远程仓库**对应分支（如 `develop`、`bugfix/*`、`master`）后，GitLab 根据 `.gitlab-ci.yml` **自动**创建并执行流水线，完成构建镜像、推送到私有仓库、执行部署脚本；无需在 GitLab 界面手动点击运行。

生成或说明文档时需**强调上述顺序**，并在「快速开始」或「开发流程」中把「本地 Docker 构建测试」放在「Git 推送触发流水线」之前。

**项目仓库地址**：默认为 **git.tac.hillstonenet.com**。克隆地址格式：`https://git.tac.hillstonenet.com/<组名>/<项目名>.git` 或 `git@git.tac.hillstonenet.com:<组名>/<项目名>.git`。生成文档与示例时使用该地址。

**使用「Git 提交触发流水线」前，必须先确认后端服务/项目是否已配置远程仓库**：

- 执行 `git remote -v` 检查是否已配置 remote（如 `origin`），且地址指向 **git.tac.hillstonenet.com** 上的项目。
- **若未配置远程仓库或 remote 不是上述地址**：应**提示用户先创建或关联远程仓库**，例如：
  - `git remote add origin https://git.tac.hillstonenet.com/<组名>/<项目名>.git` 或 SSH 形式 `git@git.tac.hillstonenet.com:<组名>/<项目名>.git`；
  - 若已有 origin 但地址错误：`git remote set-url origin <正确地址>`；
  - 说明「只有将代码推送到 git.tac.hillstonenet.com 远程仓库的 develop / bugfix / hotfix / master 分支后，流水线才会自动触发」。
- 生成项目内说明文档（如 `docs/GITLAB-CICD.md`）时，在「前置配置」或「触发方式」处写明：需先确保项目已关联 **git.tac.hillstonenet.com** 远程仓库，再通过 `git push` 触发流水线；并引用或嵌入**详细且可自动执行的 Git 操作说明**（见 [assets/git-operations.md](assets/git-operations.md)）。

### 1. 确认范围

向用户确认：

- **阶段与 Job**：是否采用 build + deploy；是否需要「依赖镜像」与「应用镜像」分离（多阶段 Docker）
- **分支策略**：develop / bugfix / hotfix / master 的用途与触发规则
- **部署目标**：**必须为 dev → prod 两环境，且必须使用 K8s 部署**。开发环境由 dev_deploy 执行（develop/bugfix/hotfix 触发），生产环境由 prod_deploy 执行（仅 master 触发）；脚本名为 `dev_deploy.sh`、`prod_deploy.sh`，在 `.gitlab-ci.yml` 的 deploy 阶段调用；命名空间（如 `api-server`）、ConfigMap（`${CI_PROJECT_NAME}-env`）、imagePullSecrets（`docker-registry`）、部署模板（如 `dev_deployment.yaml.tpl`）见 [assets/k8s/dev_deployment.yaml.tpl](assets/k8s/dev_deployment.yaml.tpl) 与 [assets/scripts/dev_deploy.sh.example](assets/scripts/dev_deploy.sh.example)。
- **私有镜像仓库**：推送地址默认为 **registry.dic.hillstonenet.com**，命名空间为 **private**（完整镜像如 `registry.dic.hillstonenet.com/private/<项目名>:latest`）；若用户无特别说明，生成 .gitlab-ci.yml 与文档时使用该地址；需明确 CI 内登录方式（变量/凭证）、部署机拉取前是否需 `docker login`
- **依赖管理**：是否使用 uv + pyproject.toml + uv.lock；依赖变更时是否单独构建「依赖镜像」以加速后续构建

### 2. 流水线设计要点

- **build 阶段**
  - **build_env**（可选）：仅在依赖文件（如 `Dockerfile`、`pyproject.toml`、`uv.lock`）变更时执行；使用 Dockerfile 的 `--target requirement` 构建依赖阶段镜像并打标签，供后续复用。
  - **build_project**：构建最终应用镜像（`--target project`）；依赖未变更时复用 build_env 的缓存，避免重复执行依赖安装。
- **deploy 阶段**
  - **push_image**：给镜像打标签并推送到**私有镜像仓库**（registry.dic.hillstonenet.com/private/<项目名>）；CI 中需先登录该仓库（`docker login registry.dic.hillstonenet.com` + 变量中的账号密码），再执行 `docker push`。
  - **dev_deploy**：在 develop / bugfix / hotfix 上执行 **K8s 部署**；调用 `scripts/dev_deploy.sh`，切换 kubectl context 到 dev 集群，按需创建/更新 ConfigMap（`${CI_PROJECT_NAME}-env`），用 `envsubst` 处理 `dev_deployment.yaml.tpl`（变量 `${CI_PROJECT_NAME}`）生成 manifest 后 `kubectl apply` 并 `kubectl rollout restart`。模板需含 Deployment、Service、Ingress（dev 域名如 `${CI_PROJECT_NAME}.apistest.dic.hillstonenet.com`，ingressClassName: api-server）。
  - **prod_deploy**：仅在 **master** 上执行 **K8s 生产环境部署**；调用 `scripts/prod_deploy.sh`，切换 context 到 prod 集群，同样通过模板 + envsubst + kubectl apply 部署；不在此分支跑 build，使用已有镜像。

分支与 Job 的对应关系见 [references/REFERENCE.md](references/REFERENCE.md) 及 [assets/pipeline-overview.md](assets/pipeline-overview.md)。

### 3. Docker 多阶段构建

若采用「依赖与代码分离」：

- **Python 基础镜像**：Python 项目的 Dockerfile 默认使用私有镜像源中的基础镜像 **docker.dic.hillstonenet.com/library/python:3.12-slim**（即 `FROM docker.dic.hillstonenet.com/library/python:3.12-slim`），以保证构建与运行环境一致且不依赖公网。
- **requirement 阶段**：在上述基础镜像上安装 uv，复制 `pyproject.toml`、`uv.lock` 并 `uv sync`；产出仅含依赖的中间镜像。CI 中 build_env 使用 `--target requirement` 构建并推送该镜像。
- **project 阶段**：在 requirement 基础上复制应用代码、设置启动命令；产出可运行的应用镜像。build_project 使用 `--target project` 构建。

本地等价命令示例见 [assets/docker-build-commands.md](assets/docker-build-commands.md)。

### 4. 分支约定与 Git 操作

- **develop**：主开发分支；推送触发 build（依赖变更时先 build_env）→ build_project → push_image → dev_deploy。
- **bugfix/***：从 develop 拉取；触发 build_project → push_image → dev_deploy；合并回 develop。
- **hotfix/***：从 master 拉取；**不触发 build**，仅 push_image → dev_deploy；需保证镜像已由 develop 等构建过；合并回 master 与 develop。
- **master**：生产就绪；**仅**推送触发 prod_deploy，不跑 build。

生成文档时应包含：**(1) 先：本地 Docker 构建测试**的命令与说明（明确写「先本地构建并验证通过，再推送」）；(2) **再：通过 Git 提交触发流水线**的说明（推送后自动触发、无需手动运行）；(3) **详细且可自动执行的 Git 操作说明**：各分支场景以**可直接复制执行的命令块**或**可执行脚本**形式给出（仓库地址使用 **git.tac.hillstonenet.com**），包括：检查/配置远程、克隆、日常 develop 提交、bugfix 创建/推送/合并回 develop、hotfix 创建/推送/合并回 master 与 develop、develop 合并到 master 发布生产；每步对应流水线结果；(4) **若未配置远程仓库**，提示先执行 `git remote add origin https://git.tac.hillstonenet.com/<组名>/<项目名>.git`（或 SSH 形式）或 `git remote set-url origin ...`。可参考 [assets/git-operations.md](assets/git-operations.md)。

### 5. 私有镜像仓库与部署后 Docker 使用

- **私有镜像仓库**：推送地址为 **registry.dic.hillstonenet.com**，命名空间 **private**。生成或校验时需包含：
  - **CI 内**：在需要 push 的 Job（build_env、push_image 等）中，于 `docker push` 前执行 `docker login registry.dic.hillstonenet.com`，账号密码从 GitLab CI/CD Variables 读取（如 `REGISTRY_USER`、`REGISTRY_PASSWORD`，设为 Masked），且不在日志中明文输出密码。
  - **镜像命名**：统一使用完整地址 `registry.dic.hillstonenet.com/private/<项目名>:<标签>`（如 `registry.dic.hillstonenet.com/private/myapp:latest`），并在文档与示例中写明。
  - **部署/运维侧**：在需拉取镜像的机器上，先执行 `docker login registry.dic.hillstonenet.com -u <用户> -p <密码>`，再 `docker pull registry.dic.hillstonenet.com/private/<项目名>:latest`；文档中应说明「使用私有仓库时需先登录」及建议的凭证管理方式。

流水线完成后，镜像已推送到私有仓库。需在文档中说明：

- **拉取镜像**：使用私有仓库时，先 `docker login registry.dic.hillstonenet.com`，再 `docker pull registry.dic.hillstonenet.com/private/<项目名>:latest`。
- `docker run` 示例：端口映射、环境变量（ENV、SECRET_KEY、数据库、Redis 等）、开发/生产模式（如 ENV=dev 用 Flask，ENV=prod 用 Gunicorn）。
- 可选：`--env-file`、`--restart unless-stopped`、常用运维命令（logs、stop、更新镜像后重建容器）。

### 6. 交付物清单

按需生成或更新：

1. **.gitlab-ci.yml**：阶段、Job、only/except 或 rules（changes/refs）、依赖关系；**默认 Runner tags** 为 `grunner`（`default.tags: [grunner]`），保证所有 Job 在指定 Runner 上执行。
2. **Dockerfile**：多阶段 target（requirement、project）、与 CI Job 的对应；Python 项目基础镜像默认 **docker.dic.hillstonenet.com/library/python:3.12-slim**。
3. **分支与流水线说明文档**：**强调先本地 Docker 构建测试、再 Git 推送触发流水线**；说明 (1) **先**本地 Docker 构建测试方式（含命令与验证通过后再推送的提示），(2) **再**通过 Git 提交触发流水线（推送后自动触发）、(3) 使用流水线前需配置 **git.tac.hillstonenet.com** 远程仓库（若无则提示创建/关联）；阶段/Job 表、分支约定表；**Git 操作说明需详细且可自动执行**（各场景为可复制执行的命令块或可执行脚本，仓库地址 git.tac.hillstonenet.com），见 [assets/git-operations.md](assets/git-operations.md)。可参考项目内 `docs/GITLAB-CICD.md` 类文档结构。
4. **部署脚本与 K8s 模板**：**必须**提供 dev → prod 的 K8s 部署方式。`scripts/dev_deploy.sh`、`scripts/prod_deploy.sh` 参考 [assets/scripts/dev_deploy.sh.example](assets/scripts/dev_deploy.sh.example)、[assets/scripts/prod_deploy.sh.example](assets/scripts/prod_deploy.sh.example)（kubectl context 切换、ConfigMap 检查/创建、envsubst + 模板生成 manifest、kubectl apply、rollout restart）；项目内需提供 `k8s/dev_deployment.yaml.tpl`（及可选 `k8s/prod_deployment.yaml.tpl`），内容参考 [assets/k8s/dev_deployment.yaml.tpl](assets/k8s/dev_deployment.yaml.tpl)（Deployment + Service + Ingress，变量 `${CI_PROJECT_NAME}`，镜像 `docker.dic.hillstonenet.com/private/${CI_PROJECT_NAME}:latest`，命名空间 `api-server`）。模板路径在 Runner 上可为固定路径（如 `/.flaskserver/dev_deployment.yaml.tpl`）或使用项目内 `k8s/`。
5. **流水线完成后使用说明**：说明 dev 与 prod 均为 K8s 部署；访问地址（dev 如 `https://<项目名>.apistest.dic.hillstonenet.com`）、ConfigMap/环境变量、常用 kubectl 命令。详见 [assets/k8s/k8s-deploy-usage.md](assets/k8s/k8s-deploy-usage.md)。

## 资产与参考

- 阶段/Job 与分支对应：[references/REFERENCE.md](references/REFERENCE.md)、[assets/pipeline-overview.md](assets/pipeline-overview.md)
- **私有镜像仓库**（CI 登录、镜像命名、部署侧拉取）：[references/REFERENCE.md](references/REFERENCE.md) 中「私有镜像仓库」小节
- .gitlab-ci.yml 示例结构（含私有仓库登录）：[assets/gitlab-ci-example.yml](assets/gitlab-ci-example.yml)
- 本地 Docker 多阶段构建命令：[assets/docker-build-commands.md](assets/docker-build-commands.md)
- **Python 基础镜像**（默认 FROM）：[assets/dockerfile-python-base.md](assets/dockerfile-python-base.md)（docker.dic.hillstonenet.com/library/python:3.12-slim）
- **K8s 部署（dev → prod，必须）**：Dev 模板 [assets/k8s/dev_deployment.yaml.tpl](assets/k8s/dev_deployment.yaml.tpl)（Deployment + Service + Ingress，`${CI_PROJECT_NAME}`、命名空间 api-server、镜像 docker.dic.hillstonenet.com/private/${CI_PROJECT_NAME}:latest、ConfigMap ${CI_PROJECT_NAME}-env、Ingress host ${CI_PROJECT_NAME}.apistest.dic.hillstonenet.com）；部署脚本示例 [assets/scripts/dev_deploy.sh.example](assets/scripts/dev_deploy.sh.example)、[assets/scripts/prod_deploy.sh.example](assets/scripts/prod_deploy.sh.example)（context 切换、ConfigMap、envsubst、kubectl apply、rollout restart）；使用说明 [assets/k8s/k8s-deploy-usage.md](assets/k8s/k8s-deploy-usage.md)。可选通用模板 [assets/k8s/deployment-template.yaml](assets/k8s/deployment-template.yaml)、[scripts/k8s-deploy.sh](scripts/k8s-deploy.sh)。
- **Git 操作说明**（详细、可自动执行，仓库 git.tac.hillstonenet.com）：[assets/git-operations.md](assets/git-operations.md)（检查/配置远程、克隆、develop/bugfix/hotfix/master 各场景命令块）
- 若项目内已有「Git 使用说明」或 AGENTS.md，生成的分支与部署说明应与之一致
