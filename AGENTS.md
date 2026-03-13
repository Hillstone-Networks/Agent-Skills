# AGENTS.md — Hillstone Networks Agent Skills

> 本文件为在本仓库工作的 AI 助手提供共享记忆。请保持内容准确并随项目演进更新。仅追加条目；未经团队同意勿删除已有内容。从最小集开始，随项目发展逐步补充。

---

## 项目概览

**名称：** Hillstone Networks Agent Skills  
**描述：** 山石网科官方 Agent Skills 仓库，基于 [vercel-labs/skills](https://github.com/vercel-labs/skills) 生态，为 Cursor、Claude Code、OpenCode、Codex 等 40+ 种 AI 编程助手提供可复用的技能指令集。  
**类型：** 技能仓库（非应用项目）

---

## 项目初始化完成后的协作重点

**在已用 project-initializer 完成初始化的项目中协作时**：无需再关注「如何初始化」「脚手架步骤」「Phase 1–3 的访谈与生成流程」等初始化方法；**只需关注开发过程中的规范与原则性内容**，例如：

- **编码与分层**：按项目类型遵循对应约定（如 Flask 的 `references/flask-backend-codegen.md`、React 的 `references/frontend-codegen.md`）— 复用优先、路由/Service 分层、测试先行、配置进 .env.example 等。
- **功能实现/修改后的测试（必须）**：功能实现或代码修改后**必须**补充或运行小范围单元测试（单函数、单组件、单接口等），保证改动可验证、可回归。**前后端都有改动时，必须进行集成测试**（端到端或接口联调），确认前后端协作正常后再合入。
- **CI/质量**：遵循该项目的 README、AGENTS.md 中已写明的质量门禁、分支策略、SDD 忽略标签，不重做初始化阶段的 CI 配置。
- **测试与排错**：若项目引用了 QA 规范，按「先根因、后修复」与用例/自动化约定执行，不回头改初始化流程。
- **多角色/子代理**：若项目已配置 .cursor/agents/*.md，按既有角色与 handoff 协作，无需重新跑角色规划。

即：**初始化是一次性的；日常协作以「开发规范 + 原则」为主，不重复、不纠结初始化细节。**

---

## 仓库结构

```
Agent-Skills/
├── README.md           # 仓库说明、安装方式、技能列表
├── AGENTS.md           # 本文件 — Agent 共享记忆
└── skills/
    └── project-initializer/
        ├── SKILL.md
        ├── scripts/    # 安装与 SDD 初始化、validate_flask_structure、validate_roles、check_route_layer
        ├── references/ # OpenSpec / SpecKit / GSD / flask-backend / backend-python-cicd /
        │               # frontend-codegen / flask-backend-codegen / qa-testing / agent-roles
        └── assets/
            ├── templates/   # README、AGENTS、AGENTS.react、AGENTS.taro、gitlab-ci、github-actions
            ├── flask-backend/
            ├── backend-python-cicd/
            ├── flask-backend-codegen/
            ├── agent-roles/
            └── scripts/     # CI 用校验脚本（tag、SDD）
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
| **project-initializer** | 一站式项目脚手架：README、AGENTS、CI/CD；项目类型「通用 / Flask 后端 / React 前端 / Taro 小程序」及对应初始化内置于本技能。可选 Python+GitLab（backend-python-cicd）、QA/测试规范、多角色与子代理；后续开发约定（frontend-codegen、flask-backend-codegen）见本技能 references。支持 OpenSpec、SpecKit、GSD 等 SDD，文档默认中文。 |

（已下线并并入 project-initializer：init-flask-backend、init-react-frontend、init-taro-miniapp、backend-python-cicd、frontend-codegen、flask-backend-codegen、qa-and-testing、agent-roles-and-subagents。）

---

## Agent 记忆日志

<!-- 在此追加重要决策或发现，格式：- [YYYY-MM-DD] 内容 -->
- [2025-03-13] 将 init-flask-backend、init-react-frontend 重新封装进 project-initializer：Phase 1 增加「项目类型」（通用/Flask 后端/React 前端/其他），Phase 2 内联 Flask 与 React 初始化流程与资产；Flask 参考与 assets 迁至 project-initializer；新增 AGENTS.react.template.md；删除 init-flask-backend、init-react-frontend 技能目录。
- [2025-03-13] 将其余技能全部并入 project-initializer：init-taro-miniapp（项目类型 Taro 小程序、AGENTS.taro.template.md）、backend-python-cicd（references/backend-python-cicd.md、assets/backend-python-cicd/）、frontend-codegen、flask-backend-codegen、qa-and-testing、agent-roles-and-subagents（各 references 与 assets 迁入）；Phase 1 增加问题 11–13（Python+GitLab 规范、QA 规范、多角色/子代理）；Phase 2 增加对应生成与衔接说明。删除 init-taro-miniapp、backend-python-cicd、frontend-codegen、flask-backend-codegen、qa-and-testing、agent-roles-and-subagents 技能目录。
