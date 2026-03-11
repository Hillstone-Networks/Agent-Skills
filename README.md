# Hillstone Networks Agent Skills

山石网科（Hillstone Networks）官方 Agent Skills 仓库，基于 [vercel-labs/skills](https://github.com/vercel-labs/skills) 生态，为各类 AI 编程助手提供可复用的技能指令集。

## 什么是 Agent Skills？

Agent Skills 是可复用的指令集，用于扩展编码助手的专项能力。每个技能由包含 `name` 与 `description` 的 `SKILL.md`（含 YAML frontmatter）定义，可被 Cursor、Claude Code、OpenCode、Codex 等 40+ 种 Agent 识别与加载。

## 安装

使用 [skills CLI](https://github.com/vercel-labs/skills) 从本仓库安装技能：

```bash
# GitHub 简写
npx skills add Hillstone-Networks/Agent-Skills

# 完整 GitHub URL
npx skills add https://github.com/Hillstone-Networks/Agent-Skills
```

### 安装选项

| 选项 | 说明 |
|------|------|
| `-g, --global` | 安装到用户目录，对所有项目生效 |
| `-a, --agent <agents...>` | 仅安装到指定 Agent（如 `cursor`、`claude-code`） |
| `-s, --skill <skills...>` | 仅安装指定技能（`*` 表示全部） |
| `--list` | 仅列出可用技能，不安装 |
| `-y, --yes` | 跳过确认提示 |

### 示例

```bash
# 列出本仓库中的技能
npx skills add Hillstone-Networks/Agent-Skills --list

# 只安装 project-initializer
npx skills add Hillstone-Networks/Agent-Skills --skill project-initializer

# 安装到 Cursor 并跳过确认
npx skills add Hillstone-Networks/Agent-Skills -a cursor -y
```

## 技能列表

| 技能 | 说明 |
|------|------|
| **project-initializer** | 脚手架新项目：生成 README.md、AGENTS.md、CI/CD 流水线（GitLab CI / GitHub Actions），支持 OpenSpec、SpecKit、GSD 等 SDD 工作流，文档默认中文。 |
| **init-react-frontend** | 初始化 React 前端项目：默认技术栈为 React + Ant Design + react-router + TypeScript + Zustand + Vitest + jsdom + Tailwind CSS + Axios + Vite + Rolldown，依赖采用生成时最新版本，并生成适配该项目的 AGENTS.md。 |
| **frontend-codegen** | 前端代码生成：在既有 React 项目中按规范生成功能/页面/组件；复用优先（工具与组件）、UI 与业务分层、数据化路由、测试先行（红/绿）、函数组件；新增第三方库时提供 3 选方案供确认。 |
| **init-taro-miniapp** | 初始化 Taro 小程序项目：强制使用 `npx @tarojs/cli init <projectName>` 创建项目；初始化后必须执行 npm install，再新建目录、配置接口 dev proxy、可添加/更新 README 与 AGENTS.md，不修改其余文件或配置。 |
| **backend-api-cicd** | GitLab CI + Docker 流水线：根据 GitLab CI 与 Docker 多阶段构建规范，生成或校验 `.gitlab-ci.yml`、分支约定与部署脚本；强调先本地 Docker 构建测试、再通过 Git 提交触发流水线；支持 dev → prod 的 K8s 部署（dev_deploy / prod_deploy）、私有镜像仓库与分支策略说明。 |
| **flask-backend-codegen** | Flask 后端代码生成：按项目规范生成 Flask API 代码（路由 Resource、Service、Model、Schema、权限策略与测试）；在用户要新增接口、新资源模块或按规范生成/补全后端代码时使用；遵循 RequestParser、AppResponse、分页与权限约定。 |
| **agent-roles-and-subagents** | 角色规划与子代理创建：按场景规划多角色 Agent 定义并生成可复用配置；将角色定义转为 Cursor/Claude/Codex 子代理（.cursor/agents/*.md）；执行前查询可用技能并询问用户约束；适用于多智能体团队规划与「Help me create this subagent for Cursor」类请求。 |
| **init-flask-backend** | 初始化 Flask 后端项目：按分层架构与规范搭建 Flask API 后端，包含应用工厂、Blueprint/Flask-RESTful 路由、Service/Model 分层、权限（JWT + Casbin）与统一响应；在用户要创建或生成 Flask 后端、REST API 项目时使用；支持 uv 依赖管理。 |
| **qa-and-testing** | 编写测试计划、用例、自动化脚本与测试报告；系统性排错与根因分析（先根因、后修复，禁止只治标）。在用户要设计测试策略、编写/评审用例、补充自动化、产出测试文档，或排查缺陷、分析测试失败、定位异常行为时使用。 |

## 支持的 Agent

本仓库技能遵循 [Agent Skills 规范](https://github.com/vercel-labs/skills)，可安装到 Cursor、Claude Code、OpenCode、Codex、GitHub Copilot 等 [40+ 种 Agent](https://github.com/vercel-labs/skills#supported-agents)。安装时 CLI 会自动检测本机已安装的 Agent。

## 仓库结构

```
Agent-Skills/
├── README.md           # 本文件
├── AGENTS.md           # Agent 共享记忆（本仓库维护约定）
└── skills/
    ├── project-initializer/
    │   ├── SKILL.md    # 技能定义与说明
    │   ├── scripts/    # 安装与 SDD 初始化脚本
    │   ├── references/ # OpenSpec / SpecKit / GSD 参考
    │   └── assets/
    │       ├── templates/   # README / AGENTS / CI 模板
    │       └── scripts/    # CI 用校验脚本（tag、SDD）
    ├── init-react-frontend/
    │   ├── SKILL.md    # 技能定义与说明
    │   └── assets/templates/
    │       └── AGENTS.template.md  # 生成项目用 AGENTS.md 模板
    ├── frontend-codegen/
    │   └── SKILL.md    # 前端代码生成规范（复用、分层、路由、测试先行）
    ├── init-taro-miniapp/
    │   ├── SKILL.md    # 技能定义与说明
    │   └── assets/templates/
    │       └── AGENTS.template.md  # 生成项目用 AGENTS.md 模板
    ├── backend-api-cicd/
    │   ├── SKILL.md    # GitLab CI + Docker 多阶段构建与 K8s 部署
    │   ├── references/ # 分支/阶段/Job 约定与私有仓库说明
    │   └── assets/     # .gitlab-ci 示例、Docker 构建命令、K8s 模板与部署脚本
    ├── flask-backend-codegen/
    │   ├── SKILL.md    # Flask API 代码生成（路由、Service、Model、Schema、权限、测试）
    │   └── references/ # 接口与代码规范
    ├── agent-roles-and-subagents/
    │   ├── SKILL.md    # 角色规划与 Cursor 子代理创建（场景→角色、子代理格式与最佳实践）
    │   ├── assets/     # 角色模板、场景示例、子代理模板、校验脚本
    │   └── references/
    ├── init-flask-backend/
    │   ├── SKILL.md    # Flask 后端项目脚手架（应用工厂、分层、权限、统一响应）
    │   ├── references/ # 目录结构与规范
    │   └── assets/     # 项目结构、create_app 片段、uv 使用说明
    └── qa-and-testing/
        ├── SKILL.md    # QA 与测试规范（测试计划、用例、自动化、报告）
        └── references/ # 用例格式、优先级、自动化与报告约定
```

## 相关链接

- [vercel-labs/skills](https://github.com/vercel-labs/skills) — Skills CLI 与规范
- [skills.sh](https://skills.sh) — 第三方技能发现与目录
- [Hillstone Networks](https://www.hillstonenet.com.cn/) — 山石网科官网

## License

MIT
