---
name: flask-backend-codegen
description: 项目规范生成 Flask API 后端代码（路由、Service、Model、Schema、权限策略与测试）；开发中优先使用常见中间件，配置写入 .env.example、用法在 .env 补充。在用户要新增接口、新资源模块、或按规范生成/补全后端代码时使用。
---

# Flask 后端代码生成

生成符合规范的 Flask API 代码：Resource、RequestParser、Service、Model、Schema、权限策略与测试。规范细节见 [references/REFERENCE.md](references/REFERENCE.md)。

## 何时使用

- 用户要求「新增一个 user 资源」「写一个符合项目规范的 CRUD API」
- 用户提供 `项目需求`，需要据此生成/补全路由、Service、Model、测试等

## 生成流程

### 1. 确认生成范围

向用户确认：

- **资源名与操作**：如 `users` 的列表/详情/创建/更新/删除；是否需分页
- **数据模型**：主要字段、是否软删除、与现有 Model 的关系
- **权限**：资源与动作（如 `user` + `read`/`create`/`update`/`delete`），是否需在 `policies.py` 中新增
- **已有约定**：项目内是否有 `docs/xxx.md`、接口契约或错误码表，优先遵从

### 2. 中间件与配置

- **优先使用常见中间件**：开发过程中优先选用项目内或生态内常见的中间件（如 Redis、消息队列、缓存、日志等），避免自造轮子。
- **向用户询问访问方式**：若涉及 Redis、消息队列、外部 API、数据库等，**向用户询问访问方式**（如连接串、主机/端口、认证方式、是否已有内网地址等），据此生成配置项说明与示例。
- **配置写入 .env.example**：所有相关配置项（变量名、说明、示例值或占位符）**补充到 `.env.example`**；不在代码中硬编码。
- **用法在 .env 中补充**：实际连接串、密钥、地址等**不在仓库提交**，由开发者在本地 `.env` 中填写；在文档或注释中说明「具体用法/取值请在 `.env` 中补充」。

### 3. 查阅规范

- 若存在 **docs/xx规范.md**：优先读取其中的接口规范、分页格式、错误码、DB 命名、权限元组、RequestParser 约定。
- 无则按 [references/REFERENCE.md](references/REFERENCE.md) 的通用约定生成。

### 4. 按规范生成代码

生成顺序与要点：

1. **权限策略**  
   在 `app/permission/policies.py` 中补充资源与操作（如 `(role, resource, action)`）；如需同步到 Casbin，提示执行 `flask sync-permissions`。

2. **Model**  
   - 继承 `db.Model`，显式 `__tablename__`（小写下划线）。
   - 必须含 `id`、`created_at`、`updated_at`；可选 `deleted_at`（软删除）。
   - 不写业务规则，仅表结构与简单查询封装。

3. **Schema**  
   请求/响应校验（Marshmallow 或 RequestParser）；与接口字段一致。

4. **Service**  
   - 所有业务逻辑、事务、外部调用放在 Service。
   - 接收路由传入的普通参数与 `user_id` 等，不直接依赖 `request`/`g`。
   - 可注入 `db` 做 ORM；列表方法返回 `(list, total)` 供分页。

5. **路由（Resource）**  
   - 每个模块 `*_api.py`：Blueprint + Api，Resource 类。
   - **RequestParser**：GET 用 `location='args'`，POST/PUT/PATCH 用 `location='json'`；分页统一 `page`、`size`。
   - 需鉴权接口加 `@permission_required(resource, action)`。
   - 仅做：解析参数 → 调 Service → 用 `AppResponse`/`AppException` 返回；禁止在路由中写 SQL/ORM 或复杂业务。

6. **响应格式**  
   - 成功：`AppResponse(data=...)`；列表分页：`data` 含 `page`、`size`、`list`、`total`。
   - 业务异常：`AppException(code=..., message=...)`；错误码段见 REFERENCE。

7. **测试**  
   - `tests/test_api_*.py`：接口测试；`tests/test_service_*.py`：业务逻辑测试。
   - `conftest.py` 提供 app、client、db 等 fixture。
   - 测试方法命名：`test_{场景}_{预期}`。

### 5. 代码规范

- Python 3.12+；类型注解；PEP 8，建议 Ruff。
- 文件名小写下划线；类名大驼峰；函数/变量小写下划线；常量全大写下划线。
- 导入顺序：标准库 → 第三方 → 本地模块，空行分隔。
- 禁止：硬编码密钥/密码；在路由层直接写 SQL/ORM；绕过 Casbin 做权限判断；信任前端传参做权限。
- **配置与中间件**：中间件与外部服务所需配置从环境变量读取；新增配置项写入 `.env.example`（含变量名与说明），实际取值在 `.env` 中由开发者补充。

### 6. 交付物清单

单次生成应包含（按需）：

1. `app/permission/policies.py` 的变更或说明
2. `app/models/{resource}.py`（若为新资源）
3. `app/schemas/{resource}_schema.py`（若使用 Schema 校验）
4. `app/service/{resource}_service.py` 及方法
5. `app/routes/{resource}_api.py`（Resource + RequestParser + @permission_required）
6. `tests/test_api_{resource}.py` 和/或 `tests/test_service_{resource}.py`
7. 若涉及中间件或外部服务（Redis、消息队列、外部 API 等），在 `.env.example` 中补充对应变量与说明，并注明「具体用法/取值请在 `.env` 中补充」
8. 若接口/错误码有约定，同步更新 `docs/` 或 `context/` 下技术文档

## 资产与参考

- 规范与示例汇总：[references/REFERENCE.md](references/REFERENCE.md)
- 统一响应与分页格式：[assets/response-format.json](assets/response-format.json)
- 路由与 Service 代码片段：[assets/code-snippets.md](assets/code-snippets.md)
- 项目内规范：**docs/xx规范.md**（若存在，优先遵从）
- 路由层违规检查（可选）：`python scripts/check_route_layer.py app/routes/*_api.py`
