---
name: generate-agent-roles
description: 根据用户使用场景规划并生成多角色 Agent 定义；执行前先查询当前有哪些可用技能，并询问用户是否有限制或规定；包含角色划分、各角色使用要求与输出规范。在用户要创建 agent 角色、定义多智能体团队、规划系统开发/数据分析/运维等场景的角色时使用。
---

# 生成 Agent 角色定义

根据使用场景规划角色、为每个角色定义使用要求与输出规范，并按通用规范生成可复用的角色配置与说明文档。

## 何时使用

- 用户实现一个较大的项目, 可能涉及多个领域
- 只在项目的初始阶段, 正在进行中的项目不要使用

## 使用流程

### 1. 确认使用场景与约束/规定

先向用户确认：

- **主要场景**：如系统/产品开发、数据分析、运维与 SRE、安全审计、内容创作、客服与运营等
- **协作方式**：角色是否串行（需求→设计→开发）或并行（多端同时开发）
- **约束**：团队规模、必须/可选角色、已有规范或模板
- **限制或规定**：**明确询问用户是否有既定限制或规定**，例如：
  - 必须/禁止使用的技术栈、工具或输出格式
  - 公司或团队已有的开发规范、安全规范、合规要求
  - 角色数量上限、命名约定、必须包含或排除的职责
  - 与现有技能、AGENTS.md、项目文档的对齐要求

若有，将上述限制与规定写入各角色定义的「约束」或「inputExpectation」中，并在生成物中显式标注遵从了哪些规定。

若用户未说明场景，可提供选项：系统开发、数据分析、运维与发布、产品与需求、全栈小团队、客服/运营等。

### 2. 规划角色清单

结合场景从「场景→角色」映射中选取并裁剪角色，并为每个角色标明职责与产出物。可参考 [references/REFERENCE.md](references/REFERENCE.md) 中的「常见场景与角色映射」。

**示例（系统开发）**：

| 角色 | 职责概要 | 主要产出 |
|------|----------|----------|
| 产品需求分析师 | 澄清需求、写 PRD、验收标准 | PRD、用户故事、验收清单 |
| 架构设计师 | 技术选型、模块划分、接口设计 | 架构图、技术方案、API 契约 |
| 后端开发工程师 | 接口实现、数据模型、领域逻辑 | 代码、API 文档、数据模型说明 |
| 前端开发工程师 | 页面与交互、联调与体验 | 页面/组件、交互说明、联调清单 |
| 测试工程师 | 用例设计、自动化与回归 | 测试用例、测试报告、缺陷列表 |
| 运维/DevOps | 部署、监控、发布流程 | 部署文档、CI/CD、运维手册 |

其他场景（数据分析、运维、产品等）的示例见 REFERENCE.md。

### 3. 为每个角色定义规范

对每个角色填写统一结构（可用 [assets/role-template.json](assets/role-template.json)）：

- **id**：角色英文 id，如 `product-analyst`、`backend-engineer`
- **displayName**：中文或产品内显示名
- **scope**：该角色的职责范围与边界（不做什么也要写清）
- **inputExpectation**：期望的输入（上游角色产出、文档格式、必填项）
- **constraints**：必须遵守的规范（分支策略、命名、安全、性能等）
- **outputSpec**：产出物格式与质量标准（文件命名、模板、必须包含的章节/字段）
- **handoff**：产出物交给谁、以何种形式（文档链接、分支、工单）

### 4. 输出规范（通用）

每个角色生成内容需符合：

- **文档**：Markdown，含「角色名、职责、输入要求、约束、输出规范、交接说明」等节；若为 API/数据模型，需写清字段与示例
- **配置**：若生成 JSON/YAML，需符合 [assets/role-template.json](assets/role-template.json) 的字段约定，便于用 `scripts/validate_roles.py` 校验
- **术语一致**：同一项目内角色名、产出物名称、阶段名保持一致

### 5. 生成物清单

一次完整生成应包含：

1. **角色清单**（表格）：角色 id、显示名、职责一句话、主要产出
2. **各角色说明**：按 role-template 展开的 Markdown 或 JSON，可存为 `roles/<role-id>.md` 或 `roles/<role-id>.json`
3. **场景总览**：本场景下角色顺序、依赖关系、关键交接点（可画 Mermaid 或列清单）
4. **可选**：`agents.config.json` 之类汇总配置，便于导入到 Cursor/AGENTS.md 等

## 资产与参考

- 角色结构模板：[assets/role-template.json](assets/role-template.json)
- 场景→角色示例：[assets/scenario-roles-example.json](assets/scenario-roles-example.json)
- 详细场景与字段说明：[references/REFERENCE.md](references/REFERENCE.md)
- 校验生成的角色配置：`python scripts/validate_roles.py roles/*.json`

## 校验

生成 JSON 角色定义后，执行：

```bash
python scripts/validate_roles.py path/to/roles/*.json
```

通过即表示结构符合通用规范，可用于后续导入或文档生成。
