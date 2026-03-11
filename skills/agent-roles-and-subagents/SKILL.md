---
name: agent-roles-and-subagents
description: 规划多角色 Agent 定义并生成可复用配置；将角色定义转为 Cursor/Claude/Codex 子代理（.cursor/agents/*.md）。执行前查询可用技能并询问用户约束。适用于多智能体团队规划、系统开发/数据分析/运维场景角色划分，以及「Help me create this subagent for Cursor」类请求。参考 Cursor 子代理文档约定。
---

# Agent 角色规划与子代理创建

本技能做两件事：**一、按场景规划并生成多角色定义**（JSON/MD + 校验）；**二、将角色定义转为 Cursor 子代理**（或兼容的 Claude/Codex 子代理）。子代理是专门化的 AI 助手，主 Agent 可将任务委派给它们，在独立上下文中运行并返回结果。格式与行为遵循 [Cursor 子代理文档](https://cursor.com/cn/docs/subagents)。

用户说「Help me create this subagent for Cursor」或明确要基于某角色创建子代理时，走「第二部分：创建子代理」。

---

## 何时使用本技能

| 场景 | 说明 |
|------|------|
| 规划多角色 | 新项目、多领域，需划分角色、职责与产出，生成角色清单与各角色规范（JSON/MD） |
| 创建子代理 | 已有角色定义（如 `backend-engineer.json`），要生成 Cursor 子代理文件（.md） |
| 阶段建议 | 角色规划建议在项目初始阶段；进行中项目仅在有明确需求时做增量角色或子代理 |

### 子代理 vs 技能（何时用哪个）

按 Cursor 文档，二者适用场景不同：

| 更适合用子代理… | 更适合用技能… |
|----------------|----------------|
| 长时间研究、需上下文隔离 | 单一用途（如生成 changelog、格式化） |
| 需并行运行多个工作流 | 快速、可重复的一次性操作 |
| 多步骤且需专业知识 | 任务可一次性完成 |
| 需对结果做独立验收/校验 | 不需要单独上下文窗口 |

若只是简单、单一用途（如「生成 changelog」「整理 import」），建议用 [Skill](https://cursor.com/docs/skills)，不必建子代理。

---

## 第一部分：生成角色定义

### 1. 确认场景与约束

向用户确认并记录：

- **场景**：系统/产品开发、数据分析、运维与 SRE、安全审计、内容创作、客服与运营等（未说明时可给选项）
- **协作**：串行（需求→设计→开发）或并行（多端同时开发）
- **规模与角色**：团队规模、必选/可选角色、已有规范或模板
- **限制与规定**（务必询问）：技术栈/工具/输出格式限制、公司或团队规范、角色数量与命名、与现有技能/AGENTS.md/项目文档的对齐要求

若有规定，写入各角色的「约束」或「inputExpectation」，并在生成物中标注遵从项。

### 2. 规划角色清单

按场景从 [references/REFERENCE.md](references/REFERENCE.md) 的「常见场景与角色映射」选取并裁剪角色，为每个角色标明职责与主要产出。

**示例（系统开发）**：

| 角色 id | 显示名 | 职责概要 | 主要产出 |
|---------|--------|----------|----------|
| product-analyst | 产品需求分析师 | 澄清需求、PRD、验收标准 | PRD、用户故事、验收清单 |
| architect | 架构设计师 | 技术选型、模块与接口设计 | 架构图、技术方案、API 契约 |
| backend-engineer | 后端开发工程师 | 接口、数据模型、领域逻辑 | 代码、API 文档、数据模型说明 |
| frontend-engineer | 前端开发工程师 | 页面与交互、联调与体验 | 页面/组件、交互说明、联调清单 |
| qa-engineer | 测试工程师 | 用例、自动化与回归 | 测试用例、测试报告、缺陷列表 |
| devops-engineer | 运维/DevOps | 部署、监控、发布流程 | 部署文档、CI/CD、运维手册 |

### 3. 为每个角色填规范

使用 [assets/role-template.json](assets/role-template.json) 结构，为每个角色填写：`id`、`displayName`、`scope`、`inputExpectation`、`constraints`、`outputSpec`、`handoff`（详见 REFERENCE 与模板）。

### 4. 输出与质量

- **文档**：Markdown，含角色名、职责、输入要求、约束、输出规范、交接说明；API/数据模型需写清字段与示例
- **配置**：JSON/YAML 符合 role-template，可用 `scripts/validate_roles.py` 校验
- **一致性**：同一项目内角色名、产出物名、阶段名保持一致

### 5. 生成物清单

一次完整生成应包含：**(1)** 角色清单表；(2) 各角色说明（建议 `roles/<role-id>.md` 或 `roles/<role-id>.json`）；**(3)** 场景总览（角色顺序、依赖、交接点，可 Mermaid）；**(4)** 可选 `agents.config.json` 等汇总配置。

### 校验

```bash
python scripts/validate_roles.py path/to/roles/*.json
```

通过即表示结构符合规范，可继续用于创建子代理。

---

## 第二部分：创建子代理

**触发**：用户说「Help me create this subagent for Cursor」或要求基于某角色定义（如 `backend-engineer.json`）创建子代理。默认平台为 Cursor；格式兼容 Claude/Codex（见下方「文件位置」）。

子代理在独立上下文中运行，可并行、可复用；Agent 会根据 `description` 决定是否委派，也可通过 `/name` 或自然语言显式调用。

### 1. 确认目录与位置

- **先确认项目是否已有子代理目录**；无则创建并在该目录下写入子代理。默认使用 **项目级** 目录。
- **文件位置**（与 [Cursor 文档](https://cursor.com/cn/docs/subagents) 一致）：

| 类型 | 位置 | 适用范围 |
|------|------|----------|
| 项目子代理 | `.cursor/agents/` | 仅当前项目（推荐，可版本管理） |
| | `.claude/agents/` | 仅当前项目（Claude 兼容） |
| | `.codex/agents/` | 仅当前项目（Codex 兼容） |
| 用户子代理 | `~/.cursor/agents/` | 当前用户所有项目 |
| | `~/.claude/agents/` | 当前用户所有项目（Claude） |
| | `~/.codex/agents/` | 当前用户所有项目（Codex） |

名称冲突时：**项目优先于用户**；同目录下 **`.cursor/` 优先于 `.claude/`、`.codex/`**。未指定时默认使用项目级 `.cursor/agents/`。

### 2. 从角色定义生成子代理

- **输入**：角色定义文件（如 `backend-engineer.json` 或 `roles/<role-id>.json`）。
- **步骤**：(1) 读取 JSON 中的 `id`、`displayName`、`scope`、`inputExpectation`、`constraints`、`outputSpec`、`handoff`；(2) 按下方格式生成 `.md` 文件；(3) 写入已确认的目录。文件名建议与 `name` 一致，如 `backend-engineer.md`。

### 3. 子代理文件格式

每个子代理一个 **Markdown 文件**，含 YAML frontmatter + 正文（system prompt）。与 Cursor 官方格式一致。

#### Frontmatter 配置字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 推荐 | 唯一标识，**小写字母与连字符**，与角色 `id` 一致；不填则默认为文件名（去扩展名） |
| `description` | 推荐 | **何时委派给该子代理**。Agent 据此决定是否委派；可写 "use proactively"、"always use for …" 等促进自动委派 |
| `model` | 否 | `fast`、`inherit` 或具体模型 ID；默认 `inherit` |
| `readonly` | 否 | 为 `true` 时子代理以受限写入权限运行 |
| `background` | 否 | 为 `true` 时子代理在后台运行，不阻塞父代理 |

**正文**：Markdown 形式的 system prompt，由角色定义转写，包含：职责与边界（scope）、期望输入（inputExpectation）、必须遵守的约束（constraints）、产出物与质量标准（outputSpec）、交接说明（handoff）。保持**简洁、具体**，避免冗长。

模板参考：[assets/subagent-cursor-template.md](assets/subagent-cursor-template.md)。

### 4. 使用方式（与 Cursor 文档一致）

- **自动委派**：Agent 根据任务复杂度、子代理的 `description` 和当前上下文决定是否委派。
- **显式调用**：在提示中用 `/name`，如 `/verifier confirm the auth flow`；或在对话中自然提及「用 verifier 子代理确认……」。
- **并行**：可同时启动多个子代理处理不同部分。

### 5. 最佳实践与反模式（来自 Cursor 文档）

**建议**：每个子代理只负责一类事、职责清晰；花精力写好 `description`；提示简洁直接；将 `.cursor/agents/` 纳入版本控制；可先让 Agent 起草再自行打磨。

**避免**：创建大量泛泛的「万能」子代理；`description` 含糊（如 "Use for general tasks"）；提示词过长；与单一用途 slash command 重复；子代理数量过多（建议先从 2–3 个聚焦明确的开始）。

### 6. 小结

| 项目 | 要求 |
|------|------|
| 平台/目录 | 默认 Cursor、项目级 `.cursor/agents/`；兼容 .claude/.codex |
| 先决检查 | 确认/创建子代理目录后再写入 |
| 格式 | .md，YAML frontmatter（name, description, model, readonly, background）+ Markdown 正文 |
| name | 小写字母与连字符 |
| description | 具体，且说明何时委派给该子代理 |

---

## 资产与参考

| 资源 | 用途 |
|------|------|
| [assets/role-template.json](assets/role-template.json) | 角色 JSON 结构模板 |
| [assets/scenario-roles-example.json](assets/scenario-roles-example.json) | 场景→角色示例 |
| [assets/subagent-cursor-template.md](assets/subagent-cursor-template.md) | 子代理 .md 转写参考 |
| [references/REFERENCE.md](references/REFERENCE.md) | 场景与角色映射、字段说明、依赖顺序 |
| [Cursor 子代理文档](https://cursor.com/cn/docs/subagents) | 子代理概念、位置、格式、最佳实践 |
| `scripts/validate_roles.py` | 校验角色 JSON：`python scripts/validate_roles.py roles/*.json` |
