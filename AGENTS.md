# AGENTS.md — Hillstone Networks Agent Skills

> 本文件为在本仓库工作的 AI 助手提供共享记忆。请保持内容准确并随项目演进更新。仅追加条目；未经团队同意勿删除已有内容。从最小集开始，随项目发展逐步补充。

---

## 项目概览

**名称：** Hillstone Networks Agent Skills  
**描述：** 山石网科官方 Agent Skills 仓库，基于 [vercel-labs/skills](https://github.com/vercel-labs/skills) 生态，为 Cursor、Claude Code、OpenCode、Codex 等 40+ 种 AI 编程助手提供可复用的技能指令集。  
**类型：** 技能仓库（非应用项目）

---

## 仓库结构

```
Agent-Skills/
├── README.md           # 仓库说明、安装方式、技能列表
├── AGENTS.md           # 本文件 — Agent 共享记忆
└── skills/
    ├── project-initializer/
    │   ├── SKILL.md
    │   ├── scripts/    # 安装与 SDD 初始化脚本
    │   ├── references/ # OpenSpec / SpecKit / GSD 参考
    │   └── assets/
    │       ├── templates/   # README / AGENTS / CI 模板
    │       └── scripts/    # CI 用校验脚本（tag、SDD）
    ├── init-react-frontend/
    │   ├── SKILL.md
    │   └── assets/templates/
    │       └── AGENTS.template.md
    ├── frontend-codegen/
    │   └── SKILL.md
    ├── init-taro-miniapp/
    │   ├── SKILL.md
    │   └── assets/templates/
    │       └── AGENTS.template.md
    ├── qa-and-testing/
    │   ├── SKILL.md    # 测试工程师规范（测试计划、用例、自动化、报告）
    │   └── references/ # 用例格式、优先级、自动化与报告约定
    └── <skill-name>/   # 每个技能一个目录
        └── SKILL.md    # 技能定义（含 YAML frontmatter）
```

- 技能根目录为 `skills/`，每个技能占一个子目录，目录名即技能 ID（如 `project-initializer`）。
- 技能的唯一入口为 `SKILL.md`，可包含 `assets/`、`scripts/`、`references/` 等辅助资源。

---

## 技能规范（vercel-labs/skills）

- **SKILL.md** 必须包含 YAML frontmatter，且至少包含：
  - `name`: 技能 ID，与目录名一致，如 `project-initializer`
  - `description`: 简短描述，用于被 Agent 识别与匹配；会出现在「可用技能」列表中
- 技能内容使用 Markdown 编写，可包含步骤、占位符说明、模板路径、脚本调用方式等。
- 本仓库技能可通过 [skills CLI](https://github.com/vercel-labs/skills) 安装，例如：
  `npx skills add Hillstone-Networks/Agent-Skills`（可选 `-s <skill>`、`-a <agent>` 等）。

---

## 技术栈与资源

| 类别 | 说明 |
|------|------|
| 技能定义 | Markdown + YAML frontmatter |
| 脚本/模板 | 技能目录内可含 Python/Shell/Node 脚本及模板（如 `assets/templates/`） |
| 文档语言 | 仓库级文档以中文为主（README、本 AGENTS.md）；技能内部可按技能需求中英混合 |
| 版本控制 | Git，主分支为 `main` |

---

## 开发与维护约定

- **新增技能：** 在 `skills/` 下新建 `<skill-name>/`，至少提供 `SKILL.md`（含 `name`、`description`）；若技能需要模板或脚本，放在该技能目录内（如 `assets/`、`scripts/`）。
- **修改技能：** 只改对应技能目录内文件；若影响安装或列表展示，需同步更新根目录 `README.md` 的「技能列表」与安装说明。
- **README 同步：** 新增/下线技能时更新 README 中的技能列表表与仓库结构说明。
- **提交信息：** 建议使用 Conventional Commits（如 `feat(skills): add xxx skill`、`docs: update README skill list`）。

---

## 当前技能列表（与 README 一致）

| 技能 | 说明 |
|------|------|
| **project-initializer** | 脚手架新项目：生成 README.md、AGENTS.md、CI/CD 流水线（GitLab CI / GitHub Actions），支持 OpenSpec、SpecKit、GSD 等 SDD 工作流，文档默认中文。 |
| **init-react-frontend** | 初始化 React 前端项目：默认技术栈为 React + Ant Design + react-router + TypeScript + Zustand + Vitest + jsdom + Tailwind CSS + Axios + Vite + Rolldown，依赖采用生成时最新版本，并生成适配该项目的 AGENTS.md。 |
| **frontend-codegen** | 前端代码生成：在既有 React 项目中按规范生成功能/页面/组件；复用优先（工具与组件）、UI 与业务分层、数据化路由、测试先行（红/绿）、函数组件；新增第三方库时提供 3 选方案供确认。 |
| **init-taro-miniapp** | 初始化 Taro 小程序项目：强制使用 `npx @tarojs/cli init <projectName>` 创建项目；初始化后必须执行 npm install，再新建目录、配置接口 dev proxy、可添加/更新 README 与 AGENTS.md，不修改其余文件或配置。 |

| **qa-and-testing** | QA 与测试规范：编写测试计划、用例、自动化脚本与测试报告；在用户要设计测试策略、编写/评审用例、补充自动化或产出测试文档时使用；遵循用例 ID、步骤预期、优先级与自动化命名约定。 |
| **agent-roles-and-subagents** | 角色规划与子代理创建：按场景规划多角色定义并生成配置；将角色定义转为 Cursor 子代理（.cursor/agents/*.md）；参考 Cursor 子代理文档；适用于多智能体规划与「Help me create this subagent for Cursor」请求。 |

---

## Agent 记忆日志

<!-- 在此追加重要决策或发现，格式：- [YYYY-MM-DD] 内容 -->
