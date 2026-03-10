---
name: init-taro-miniapp
description: "Scaffolds a Taro mini-program project using the latest Taro CLI (taro init / npx @tarojs/cli init), standard component library @tarojs/components per Taro docs, and generates project-specific AGENTS.md with code-gen rules (reuse-first, unified style, third-party options, UI/business separation). Use when initializing a mini-program, Taro project, or multi-end (weapp/h5/rn) app."
---

# Init Taro 小程序

使用最新版 Taro 初始化跨端小程序项目，采用官方组件库规范，并生成带代码生成约束的 AGENTS.md。

## 参考文档

- [Taro 介绍与安装](https://docs.taro.zone/docs/)
- [安装及使用](https://docs.taro.zone/docs/GETTING-STARTED)
- [组件库说明](https://docs.taro.zone/docs/components-desc) — 使用 `@tarojs/components`，事件以 `on` 开头、组件首字母大写与驼峰命名

## 默认技术栈（未指定时）

| 类别     | 默认选择                          |
|----------|-----------------------------------|
| 框架     | Taro（最新稳定版）                |
| 语法     | React 或 Vue3（init 时可选）     |
| 语言     | TypeScript                       |
| 组件库   | @tarojs/components（Taro 标准）  |
| UI 增强  | 可选 taro-ui@next（Taro 3+）     |

用户若指定其他框架（如 Vue3、Preact），按用户选择；未指定则可用 React + TypeScript 作为默认。

## 依赖版本策略

- Taro 相关包使用 **执行技能时的最新稳定版本**。
- 生成前可查询：`npm info @tarojs/cli version`、`npm info @tarojs/taro version` 等。
- 在 `package.json` 中写入确定版本（可含 `^`，便于后续升级），并在 README 或 AGENTS.md 中说明版本为脚手架生成时选定。

## 工作流

### 1. 收集项目信息

- **项目名称与一句话描述** — 用于 README、AGENTS.md。
- **框架与语法** — React / Vue3 / Preact 等，是否 TypeScript。
- **目标端** — 微信小程序、H5、多端等（影响后续脚本与配置）。
- **文档语言** — 默认中文。

### 2. 使用最新 Taro 初始化项目

在目标目录执行（二选一）：

```bash
# 已全局安装 @tarojs/cli 时
taro init <projectName>
```

```bash
# 不全局安装，使用 npx（推荐，保证最新）
npx @tarojs/cli init <projectName>
```

- 初始化过程中按需选择：框架（React/Vue3 等）、TypeScript、CSS 预处理器、编译工具、包管理器。
- 若在已有目录内初始化，可使用当前目录名作为项目名或先创建子目录再 init。

### 3. 组件库规范（@tarojs/components）

- 组件以 [Taro 组件库说明](https://docs.taro.zone/docs/components-desc) 为准，从 `@tarojs/components` 引用。
- React 示例：

```tsx
import { View, Text } from '@tarojs/components'
```

- 规范要点：
  - 组件名**首字母大写、驼峰**（如 `Map`、`View`）。
  - 事件属性以 **on 开头**（如 `onClick`、`onTap`），与小程序 bind 写法对应。
- 可选：多端 UI 组件库 [Taro UI](https://taro-ui.jd.com/)（Taro 3+ 使用 `taro-ui@next`）。

### 4. 生成 AGENTS.md

在**已初始化的项目根目录**生成 `AGENTS.md`，使用本技能自带的 `assets/templates/AGENTS.template.md` 填充。

**占位符：**

- `{{PROJECT_NAME}}` — 项目名称
- `{{PROJECT_DESCRIPTION}}` — 一句话描述
- `{{TECH_STACK_TABLE}}` — 技术栈表（Taro、React/Vue、TS、@tarojs/components 等）
- `{{DIR_STRUCTURE}}` — 项目目录树（如 `src/`、`config/`、`dist/`）
- `{{SCRIPTS}}` — 常用脚本（如 `dev:weapp`、`build:weapp`、`dev:h5`、`build:h5` 等）及说明
- `{{INITIALIZED_DATE}}` — 初始化日期 `YYYY-MM-DD`

文档语言与项目约定一致（默认中文）。

### 5. 代码生成约束（写入 AGENTS.md）

生成的 AGENTS.md 中必须包含以下约定（模板已含，确保填充后保留）：

- **a. 优先复用已有逻辑** — 新增前先查找 `utils`、`components`、`hooks`、`api`，能复用则复用或扩展，不重复造轮子。
- **b. 代码风格统一** — 遵循项目内已有风格（命名、缩进、引号、组件写法等）。
- **c. 新增第三方库** — 须给出多个方案（至少 2–3 个），列出优缺点，由用户选择后再安装并记录。
- **d. UI 与业务组件分离** — 展示/交互组件与数据、接口、状态逻辑分层；容器/页面负责业务，纯 UI 组件只接收 props 与回调。

### 6. 后续步骤

- 在项目根目录执行 `npm install`（或所选包管理器）以确认依赖完整。
- 可选：运行 `npm run dev:weapp`（或对应端）并在开发者工具中打开 `dist` 验证。
- 告知用户项目已就绪、AGENTS.md 位置及其中代码生成约定。

## 模板路径

- **AGENTS 模板：** `assets/templates/AGENTS.template.md` — 按上述占位符填入新项目名称、技术栈、目录结构、脚本及日期。
