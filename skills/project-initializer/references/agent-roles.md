# Agent 角色定义与子代理参考

用于多角色规划与生成 Cursor/Claude/Codex 子代理（.cursor/agents/*.md）时查阅。

## 常见场景与角色映射

### 系统 / 产品开发

| 角色 id | 显示名 | 职责概要 | 主要产出 |
|---------|--------|----------|----------|
| product-analyst | 产品需求分析师 | 收集与澄清需求、编写 PRD、定义验收标准 | PRD、用户故事、验收清单、原型说明 |
| architect | 架构设计师 | 技术选型、模块划分、接口与数据模型设计 | 架构图、技术方案、API 契约、数据模型 |
| backend-engineer | 后端开发工程师 | 接口实现、领域逻辑、数据持久化与集成 | 代码、API 文档、数据模型说明、迁移脚本 |
| frontend-engineer | 前端开发工程师 | 页面与交互、状态与联调、性能与可访问性 | 页面/组件、交互说明、联调清单 |
| qa-engineer | 测试工程师 | 用例设计、自动化与回归、缺陷跟踪 | 测试用例、测试报告、缺陷列表 |
| devops-engineer | 运维/DevOps 工程师 | 部署、CI/CD、监控与发布流程 | 部署文档、流水线配置、运维手册 |

### 数据分析与算法、运维与 SRE、产品与需求、全栈小团队

详见本技能 `assets/agent-roles/` 下示例与 REFERENCE 原文；角色结构含 id、displayName、scope、inputExpectation、constraints、outputSpec、handoff。

## 角色定义结构

每个角色建议包含：id（小写连字符）、displayName、scenario、scope、inputExpectation、constraints、outputSpec、handoff、metadata。模板见本技能 `assets/agent-roles/role-template.json`。

## 创建子代理

- **目录**：项目级 `.cursor/agents/`（推荐，可版本管理）；或用户级 `~/.cursor/agents/`。兼容 `.claude/agents/`、`.codex/agents/`。
- **格式**：每子代理一个 .md 文件，含 YAML frontmatter（name、description、model、readonly、background）+ Markdown 正文（职责、输入期望、约束、产出规范、交接说明）。name 小写连字符；description 具体且说明何时委派。
- **从角色定义生成**：读取角色 JSON 的 id、displayName、scope、inputExpectation、constraints、outputSpec、handoff，按上述格式写成 .md 并写入上述目录。模板见本技能 `assets/agent-roles/subagent-cursor-template.md`。
- **校验**：角色 JSON 可用本技能 `scripts/validate_roles.py`（若已复制到项目）校验：`python scripts/validate_roles.py roles/*.json`。
- **参考**：[Cursor 子代理文档](https://cursor.com/cn/docs/subagents)。
