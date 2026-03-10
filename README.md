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

## 支持的 Agent

本仓库技能遵循 [Agent Skills 规范](https://github.com/vercel-labs/skills)，可安装到 Cursor、Claude Code、OpenCode、Codex、GitHub Copilot 等 [40+ 种 Agent](https://github.com/vercel-labs/skills#supported-agents)。安装时 CLI 会自动检测本机已安装的 Agent。

## 仓库结构

```
Agent-Skills/
├── README.md           # 本文件
└── skills/
    └── project-initializer/
        └── SKILL.md    # 技能定义与说明
```

## 相关链接

- [vercel-labs/skills](https://github.com/vercel-labs/skills) — Skills CLI 与规范
- [skills.sh](https://skills.sh) — 第三方技能发现与目录
- [Hillstone Networks](https://www.hillstonenet.com.cn/) — 山石网科官网

## License

MIT
