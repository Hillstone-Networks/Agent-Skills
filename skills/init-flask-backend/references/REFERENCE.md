# Flask API 后端规范参考

本文档提炼自《Flask API 后端项目规范》，用于生成或校验项目时查阅。

## 推荐目录结构

```
project/
├── app/
│   ├── __init__.py           # 应用工厂、初始化入口
│   ├── config.py             # 配置加载
│   ├── extensions.py         # 扩展实例（DB、Redis、Casbin 等）
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main_api.py       # 健康检查、通用接口
│   │   └── {module}_api.py   # 业务模块 API
│   ├── models/
│   ├── service/
│   ├── schemas/              # 请求/响应校验（Marshmallow 等）
│   ├── permission/           # 可选：权限
│   │   ├── constants.py
│   │   ├── policies.py
│   │   ├── decorators.py
│   │   └── manager.py
│   └── utils/
│       ├── api_util.py       # 统一响应、异常
│       ├── logger_util.py
│       └── jwt_util.py
├── docs/
├── context/
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_service.py
├── scripts/
├── .env.example
├── pyproject.toml
├── Dockerfile
├── .gitlab-ci.yml 或 .github/workflows
└── README.md
```

## UV 项目管理

- 使用 **uv** 管理依赖与虚拟环境；以 `pyproject.toml` + `uv.lock` 为权威，不依赖 `requirements.txt`。
- **常用命令**：`uv sync`（安装依赖）、`uv run flask run`（运行应用）、`uv run pytest`（测试）、`uv add <包名>`（添加依赖）。
- 用户使用说明见 skill 资产 [assets/uv-usage.md](../assets/uv-usage.md)，生成项目时可将该内容写入 README 或单独提供给用户。

## 分层架构

- **Routes**：接收请求、参数校验、调用 Service，不直接操作 DB。
- **Permission**：鉴权（JWT + RBAC/ABAC），在进入 Resource 前执行。
- **Service**：业务逻辑、事务、外部调用。
- **Model**：数据模型、ORM。
- **Infrastructure**：数据库、缓存、消息队列。

原则：路由层不直接操作数据库；Service 不依赖 `request`/`g`，通过参数接收上下文。

## Flask 与 Flask-RESTful 约定

- **应用工厂**：`create_app(config_name)`，多环境配置与测试注入。
- **Blueprint**：按业务模块拆分，`url_prefix` 如 `/api/users`；在 `create_app` 中统一注册。
- **扩展**：在 `extensions.py` 中集中定义实例，在 `create_app()` 中 `init_app`，避免循环引用。

| 概念 | 说明 |
|------|------|
| Resource | 继承 `flask_restful.Resource`，方法名对应 HTTP 方法（get/post/put/delete） |
| Api | 绑定到 Blueprint，`api.add_resource(Resource, '/path')` |
| RequestParser | 声明式参数解析与校验，`parser.parse_args()` 在 Resource 内调用 |

- **路由文件**：每个业务模块一个 `*_api.py`，创建 Blueprint 和 Api，定义 Resource；Resource 只做「解析参数 → 调 Service → 返回 AppResponse/字典」。
- **统一响应**：封装 Api 的 JSON 输出为 `{code, message, data}`，并统一错误处理。

## 请求处理流程

1. 请求进入 → 匹配 Blueprint + Api 的 URL。
2. `before_request`：JWT 解析，写入 `g.current_user`。
3. Resource 上的 `@permission_required`：权限校验，不通过 403。
4. Resource 方法：`parse_args()` → 调 Service → 返回 AppResponse/字典。
5. 自定义 Api 将返回值封装为统一结构，设置状态码，返回响应。

## 钩子顺序与职责

| 钩子 | 时机 | 典型用途 | 返回值 |
|------|------|----------|--------|
| before_request | 路由前 | 填充 g.current_user | None 放行，否则作为响应 |
| after_request | 视图返回后 | 加 X-Trace-Id、Token 刷新 | 必须返回 response |
| teardown_request | 请求上下文结束 | 请求级资源清理、记日志 | 无要求 |
| teardown_appcontext | 应用上下文 pop | 与 app 上下文相关的清理 | 无要求 |

## register_all_blueprints 约定

- 仅扫描 `app/routes` 下以 `_api.py` 结尾的模块。
- 每个模块导出的 Blueprint 变量名：文件名去掉 `_api` 后缀 + `_app`。例：`user_api.py` → `user_app`。
- 支持配置 `DISABLEPATH` 跳过指定模块；捕获导入/注册异常并打日志，避免单模块错误导致应用无法启动。

## OpenTelemetry（可选）

- 在 `create_app()` 中，在扩展与蓝图注册之前初始化 TracerProvider，使用 `FlaskInstrumentor().instrument_app(flask_app)`。
- 仅在满足条件时初始化（如 `ENV=prod` 且配置了 `TRACE_ENDPOINT`）。
- 在 `after_request` 中将当前 span 的 `trace_id` 写入 `response.headers['X-Trace-Id']`。
- 在全局 errorhandler 中记录异常时附带 `trace_id`。

## 示例：单模块路由

```python
# app/routes/user_api.py
from flask import Blueprint
from flask_restful import Resource
from app.utils.api_util import Api, AppResponse
from app.permission import permission_required

bp = Blueprint('user', __name__, url_prefix='/api/users')
api = Api(bp)

class UserListResource(Resource):
    @permission_required('user', 'read')
    def get(self):
        return AppResponse(data={"items": []})

class UserDetailResource(Resource):
    @permission_required('user', 'read')
    def get(self, user_id):
        return AppResponse(data={"id": user_id})

api.add_resource(UserListResource, '/')
api.add_resource(UserDetailResource, '/<int:user_id>')
```

应用初始化中：`app.register_blueprint(user_api.bp)`，或通过 `register_all_blueprints(app)` 自动注册。
