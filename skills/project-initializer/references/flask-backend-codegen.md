# Flask 后端代码生成规范参考

用于按规范生成路由、Service、Model、Schema、权限与测试时查阅。

## 代码规范

| 类别     | 规范说明 |
|----------|----------|
| 语言     | Python 3.12+；包管理用 uv（`uv sync`） |
| 代码风格 | PEP 8，建议 Ruff 检查/格式化；函数与返回值建议类型注解 |
| 命名     | 文件名小写下划线；类名大驼峰；函数/变量小写下划线；常量全大写下划线 |
| 导入顺序 | 标准库 → 第三方库 → 本地模块，之间空行分隔 |
| 禁止     | 硬编码密钥/密码；在路由层直接写 SQL/ORM 或复杂业务；绕过 Casbin 做权限判断；信任前端传参做权限 |

## 项目结构与分层

- **路由**：`app/routes/*_api.py`，Flask-RESTful Resource；仅做参数解析、调用 Service、返回 AppResponse/AppException。
- **Service**：`app/service/`，业务逻辑、事务、外部调用；接收路由传入参数与 user_id，不依赖 `request`/`g`。
- **Model**：`app/models/`，表结构、ORM；必须含 id、created_at、updated_at；不写业务规则。
- **Schema**：`app/schemas/`，请求/响应校验。
- **权限**：`app/permission/policies.py` 定义策略；新增/变更后执行 `flask sync-permissions`。

## 路由层约定

- 使用 Flask-RESTful **Resource**；参数用 **RequestParser**：GET 用 `location='args'`，POST/PUT 用 `location='json'`。
- 分页参数统一：`page`、`size`（缺省可 page=1、size=20）。
- 需鉴权接口加 `@permission_required(resource, action)`。
- 成功：`AppResponse(data=...)`；业务异常：`AppException(code=..., message=...)`。
- 分页列表的 `data` 结构：`{ "page", "size", "list", "total" }`。

## 接口规范（REST）

- 基础路径 `/api`；资源名小写复数；嵌套资源如 `/api/parents/:parent_id/children`。
- HTTP：GET 查询、POST 创建、PUT 全量更新、PATCH 部分更新、DELETE 删除。
- 认证：Token 放 Header（如 `Authorization: Bearer <token>`），不在 URL/body。
- 列表分页：Query 参数 `page`、`size`。

**统一响应**：`{ "code": 0, "message": "请求成功", "data": {} }`。分页时 `data` 为 `{ "page", "size", "list", "total" }`。

**业务错误码分段**：0 成功；1xxx 认证/用户；2xxx 参数校验；3xxx 业务逻辑；4xxx 资源；9999 未知/系统。HTTP 401/403/404 等与业务 code 对应。

## 数据库与 Model

- 表名：小写下划线，复数或业务名（如 `user_roles`、`order_items`）。
- 通用字段：`id`（主键）、`created_at`、`updated_at`（DateTime UTC）；可选 `deleted_at`（软删除）。
- Model 继承 `db.Model`，显式 `__tablename__`。

## 权限（Casbin RBAC）

- 元组：`(subject, object, action)`，如 (用户/角色, 资源, 操作)。
- 操作示例：`read`、`create`、`update`、`delete`、`admin`。
- 资源命名：小写、多词下划线，如 `product`、`order_item`。
- 策略在 `app/permission/policies.py` 中定义；不在路由或 Service 中绕过 Casbin。

## 测试约定

- 单测：pytest；`tests/conftest.py` 提供 app、client、db 等 fixture。
- 接口测试：`test_api_*.py`；业务逻辑：`test_service_*.py`。
- 测试方法命名：`test_{场景}_{预期}`，如 `test_login_success_returns_token`。

## 中间件与配置

- **优先使用常见中间件**：开发中优先选用项目内或生态内常见中间件（Redis、消息队列、缓存、日志等）。
- **询问访问方式**：涉及 Redis、消息队列、外部 API、数据库等时，向用户询问访问方式（连接串、主机/端口、认证方式等），据此写配置说明与示例。
- **.env.example**：所有相关配置项（变量名、说明、示例或占位符）写入 `.env.example`；不提交真实密钥与连接串。
- **.env**：实际连接串、密钥、地址等由开发者在本地 `.env` 中填写；文档或注释中说明「具体用法/取值请在 `.env` 中补充」。

## 开发流程与禁止事项

- 新功能：先查阅 docs/ 与 context/；设计 URL、请求响应、权限；在 policies.py 补充策略并 `flask sync-permissions`；实现 Service 再写路由；涉及中间件时更新 `.env.example`；更新技术文档。
- 允许修改：`app/routes/`、`app/models/`、`app/service/`、`app/permission/policies.py`、`app/schemas/`、`.env.example`。
- 禁止：修改 `app/__init__.py` 核心初始化；在路由中直接操作 db/ORM；硬编码密钥；绕过 Casbin；将真实密钥写入仓库。
