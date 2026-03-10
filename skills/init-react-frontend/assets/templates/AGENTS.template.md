# AGENTS.md — {{PROJECT_NAME}}

> 本文件为在本项目工作的 AI 助手提供共享记忆。请保持内容准确并随项目演进更新。仅追加条目；未经团队同意勿删除已有内容。

---

## 项目概览

**名称：** {{PROJECT_NAME}}  
**描述：** {{PROJECT_DESCRIPTION}}  
**类型：** 前端应用

---

## 技术栈与资源

{{TECH_STACK_TABLE}}

---

## 仓库/目录结构

```
{{DIR_STRUCTURE}}
```

- 入口：`index.html` → `src/main.tsx`
- 路由与根组件：`src/App.tsx`
- 页面组件：`src/pages/`
- 状态：`src/store/`（Zustand）
- 请求：`src/api/` 或 `src/services/`（Axios）
- 测试：Vitest，用例与源码同目录或 `src/**/*.test.{ts,tsx}`

---

## 开发与维护约定

### 脚本命令

{{SCRIPTS}}

### 代码与规范

- 使用 TypeScript，遵循项目内已有风格
- 组件与页面按功能组织在 `src/` 下
- **功能/页面/组件开发**：优先使用 **frontend-codegen** 技能（若已安装：`Hillstone-Networks/Agent-Skills` 之 `frontend-codegen`），按复用优先、UI/业务分层、数据化路由、测试先行与函数组件规范生成代码
- 新增能力时同步更新本 AGENTS.md（可追加「Agent 记忆日志」）

### 测试与构建

- 单元/组件测试：`npm run test`（Vitest + jsdom）
- 生产构建：`npm run build`，产物在 `dist/`
- 本地预览构建结果：`npm run preview`

### 文档语言

- 仓库级文档与 AGENTS.md 默认中文；若团队约定英文则按约定。

---

## Agent 记忆日志

<!-- 在此追加重要决策或发现，格式：- [YYYY-MM-DD] 内容 -->
<!-- 初始化于 {{INITIALIZED_DATE}} -->
