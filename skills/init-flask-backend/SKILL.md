---
name: init-flask-backend
description: 按分层架构与规范搭建 Flask API 后端项目，包含应用工厂、Blueprint/Flask-RESTful 路由、Service/Model 分层、权限与统一响应。在用户要创建或生成 Flask 后端、REST API 项目使用
---

# Flask API 后端项目生成

根据规范文档搭建标准 Flask API 后端：应用工厂、分层架构（Routes → Permission → Service → Model）、Flask-RESTful Resource、统一响应与钩子。详细约定见 [references/REFERENCE.md](references/REFERENCE.md)。

## 何时使用

- 用户要求「生成 Flask 后端」「搭建 REST API 项目」
- 用户需要初始化项目规范，需要据此生成/补全项目骨架与示例代码

## 生成流程

### 1. 确认范围

向用户确认：

- **项目名与包名**：如 `my_api`，对应目录 `app/`
- **是否需要权限模块**：JWT + Casbin/RBAC（可选 `permission/`）
- **是否需要链路跟踪**：OpenTelemetry + OTLP（可选，见 REFERENCE）
- **已有文件**：是否已有部分文件，仅补全缺失部分

### 2. 生成目录结构

按 [references/REFERENCE.md](references/REFERENCE.md) 的「推荐目录结构」创建完整目录树，保证以下存在：

- `app/`：`__init__.py`（应用工厂）、`config.py`、`extensions.py`
- `app/routes/`：`__init__.py`、`main_api.py`，业务模块 `*_api.py`
- `app/models/`、`app/service/`、`app/schemas/`
- 可选：`app/permission/`、`app/utils/`
- `tests/`（含 `conftest.py`）、`scripts/`、`docs/` 或 `context/`
- 根目录：`.env.example`、`pyproject.toml`（含 `[tool.uv]` 或兼容 uv）、`README.md`、可选 `Dockerfile`

可直接参考 [assets/project-structure.txt](assets/project-structure.txt)。依赖管理使用 **uv**，见 [assets/uv-usage.md](assets/uv-usage.md)。

### 3. 核心文件内容要点

- **app/__init__.py**：`create_app(config_name)` 应用工厂；初始化扩展（`extensions.py`）、加载配置、注册 Blueprint（可调用 `register_all_blueprints(app)`）、注册 `before_request`/`after_request`/`teardown_request`/`teardown_appcontext` 及全局 `errorhandler`。
- **app/config.py**：按环境（development/test/production）加载配置，敏感项从环境变量读取。
- **app/extensions.py**：集中定义 Flask-SQLAlchemy、Redis、JWT、Casbin 等扩展实例（不在此处 init_app，在 create_app 中调用）。
- **app/utils/api_util.py**：统一响应格式（如 `AppResponse`、`{code, message, data}`）、自定义 `Api` 的 JSON 封装、统一异常处理。
- **app/routes/main_api.py**：健康检查等通用接口；Blueprint 命名与 `*_api.py` 约定一致，导出 `*_app`（如 `main_app`）供自动注册。
- **业务路由**：每个模块一个 `*_api.py`，内部创建 Blueprint + Api，定义 Resource 类；Resource 仅做「解析参数 → 调 Service → 返回 AppResponse/字典」，不直接操作 Model。
- **register_all_blueprints**：实现见 REFERENCE，扫描 `app/routes` 下 `*_api.py`，按约定名（文件名去 `_api` 加 `_app`）自动 register_blueprint。

### 4. 分层与约定

- **路由层**：不直接访问 DB/Model；仅解析请求、调用 Service、返回统一结构。
- **Service 层**：业务逻辑、事务、外部调用；不依赖 `request`/`g`，通过参数接收上下文，便于单测。
- **Model 层**：仅负责 ORM 与持久化。
- **权限**：JWT 在 before_request 或中间件中解析并写入 `g.current_user`；Resource 方法上使用 `@permission_required` 等装饰器做鉴权。

### 5. 钩子与可观测性

- **before_request**：将 JWT 解析结果写入 `g.current_user`，不做重逻辑。
- **after_request**：添加 `X-Trace-Id` 等响应头，可选 Token 刷新；必须返回 response。
- **teardown_request / teardown_appcontext**：请求级/应用上下文级清理与日志。
- 若启用 OpenTelemetry：在 create_app 中按 REFERENCE 初始化 TracerProvider、instrument Flask，并在 after_request 中写 `X-Trace-Id`。

### 6. 交付物清单

生成或补全后，应包含：

1. 完整目录与占位 `__init__.py`/空文件
2. `app/__init__.py`（create_app + register_all_blueprints + 钩子）
3. `app/config.py`、`app/extensions.py`
4. `app/utils/api_util.py`（AppResponse、统一 Api）
5. `app/routes/main_api.py` 及至少一个业务模块示例（如 `user_api.py`）
6. 占位或示例的 `app/models/`、`app/service/`、`app/schemas/`
7. `.env.example`、`pyproject.toml`（含 uv 可用的依赖与脚本）、`README.md`，可选 `Dockerfile`、CI 配置
8. `tests/conftest.py` 及至少一个 API 测试示例
9. **README 或独立说明**中包含「用户如何使用」：环境准备、uv 安装与常用命令，见 [assets/uv-usage.md](assets/uv-usage.md)

## 依赖与 UV 项目管理

- 使用 **uv** 管理依赖与虚拟环境；不生成 `requirements.txt`，以 `pyproject.toml` + `uv.lock` 为准。
- **pyproject.toml**：`[project]` 中声明依赖（flask、flask-restful、flask-sqlalchemy 等）；可用 `[project.scripts]` 暴露入口如 `app = "app:create_app"`；可选 `[tool.uv]` 配置。
- 生成后提示用户按 [assets/uv-usage.md](assets/uv-usage.md) 操作：安装 uv → 进入项目 → `uv sync` → `uv run flask run` 或 `uv run pytest`。

## 资产与参考

- 规范与结构详解：[references/REFERENCE.md](references/REFERENCE.md)
- 目录树清单：[assets/project-structure.txt](assets/project-structure.txt)
- 应用工厂与 Blueprint 注册示例：[assets/create_app_snippet.py](assets/create_app_snippet.py)
- 环境变量示例：[assets/env-example.txt](assets/env-example.txt)（生成 `.env.example` 时参考）
- **用户如何使用 UV**：[assets/uv-usage.md](assets/uv-usage.md)（可整段写入 README 或单独提供给用户）
- **pyproject.toml 示例（uv）**：[assets/pyproject-uv.example.toml](assets/pyproject-uv.example.toml)

## 校验（可选）

生成后可用脚本检查必要文件与目录是否存在：

```bash
python scripts/validate_structure.py /path/to/project
```
