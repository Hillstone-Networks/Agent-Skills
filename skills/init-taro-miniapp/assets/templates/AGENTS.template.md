# AGENTS.md — {{PROJECT_NAME}}

> 本文件为在本项目工作的 AI 助手提供共享记忆。请保持内容准确并随项目演进更新。仅追加条目；未经团队同意勿删除已有内容。

---

## 项目概览

**名称：** {{PROJECT_NAME}}  
**描述：** {{PROJECT_DESCRIPTION}}  
**类型：** Taro 跨端小程序应用

---

## 技术栈与资源

{{TECH_STACK_TABLE}}

- **组件库：** 使用 [Taro 标准组件库](https://docs.taro.zone/docs/components-desc) `@tarojs/components`（View、Text、ScrollView 等）；React 需从 `@tarojs/components` 引入，事件以 `on` 开头、组件首字母大写与驼峰命名。

---

## 仓库/目录结构

```
{{DIR_STRUCTURE}}
```

- 入口与页面：以 Taro 初始化后的 `src/`、`config/` 为准
- 编译产物：`dist/`（或 config 中 `outputRoot` 指定目录）

---

## 开发与维护约定

### 脚本命令

{{SCRIPTS}}

### 代码生成与规范（AI 助手须遵守）

1. **优先复用已有逻辑**
   - 新增功能前先查找项目内已有的 `utils`、`components`、`hooks`、`api`、`services`。
   - 能复用则复用或在其基础上扩展（包装组件、增加工具函数等），避免重复实现。

2. **代码风格统一**
   - 遵循项目内已有命名、缩进、引号、组件写法等风格。
   - 与现有文件保持一致，不引入新的风格冲突。

3. **新增第三方库**
   - 需要引入新依赖时，**不得直接安装**。须先给出 **至少 2～3 个方案**，列出各方案优缺点及适用场景，由用户选择后再安装，并在 README 或本 AGENTS.md 中记录。

4. **UI 与业务组件分离**
   - **UI（展示）组件**：只负责展示与交互，通过 props 接收数据和回调，不直接调接口、不直接读全局状态。
   - **业务（容器）组件/页面**：负责数据获取、状态、业务逻辑，并把数据和回调传给 UI 组件。
   - 按功能划分目录时，将纯 UI 与业务逻辑分层放置（如 `components/` 与 `pages/` 或 `features/` 的职责区分）。

### 文档语言

- 仓库级文档与 AGENTS.md 默认中文；若团队约定英文则按约定。

---

## Agent 记忆日志

<!-- 在此追加重要决策或发现，格式：- [YYYY-MM-DD] 内容 -->
<!-- 初始化于 {{INITIALIZED_DATE}} -->
