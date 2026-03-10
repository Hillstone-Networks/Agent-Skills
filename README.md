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
| **init-taro-miniapp** | 初始化 Taro 小程序项目：使用最新版 Taro CLI（`taro init` / `npx @tarojs/cli init`）与 @tarojs/components，生成带代码生成约束的 AGENTS.md（复用优先、风格统一、第三方库多方案、UI/业务分离）。 |

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
    └── init-taro-miniapp/
        ├── SKILL.md    # 技能定义与说明
        └── assets/templates/
            └── AGENTS.template.md  # 生成项目用 AGENTS.md 模板
```

## 相关链接

- [vercel-labs/skills](https://github.com/vercel-labs/skills) — Skills CLI 与规范
- [skills.sh](https://skills.sh) — 第三方技能发现与目录
- [Hillstone Networks](https://www.hillstonenet.com.cn/) — 山石网科官网

## License

MIT
