---
name: frontend-codegen
description: "Generates React frontend code following project conventions: reuse-first (utils/components), UI vs business component split, data-driven routes, test-first (red/green), function components. When adding third-party libs, presents 3 options with pros/cons for user confirmation. Use when implementing features, pages, or components in a React + Ant Design + TypeScript + Vite project."
---

# Frontend Code Generation

Generates frontend code that aligns with the project tech stack and enforces reuse, layering, data-driven routing, and test-first workflow.

## Tech stack (default alignment)

| Category | Default |
|----------|---------|
| Framework | React (function components) |
| UI | Ant Design |
| Router | react-router-dom |
| Language | TypeScript |
| State | Zustand |
| Test | Vitest + jsdom |
| Style | Tailwind CSS |
| HTTP | Axios |
| Build | Vite |

When generating code, use these unless the project explicitly uses different choices.

---

## 1. Third-party library selection

**When introducing a new third-party dependency**, do not add it directly. Instead:

1. **Propose exactly 3 options** (different libraries or approaches).
2. **For each option list**:
   - Name and npm package (if applicable)
   - Pros (2–4 bullets)
   - Cons (2–4 bullets)
   - Brief use-case fit
3. **Ask the user to choose** (e.g. "请确认使用选项 A/B/C，或说明其他偏好").
4. **Only add the chosen dependency** after user confirmation; then document in README or AGENTS.md if relevant.

**Example format:**

```markdown
## 新增 [功能] 的依赖方案

| 选项 | 库名 | 优点 | 缺点 | 适用场景 |
|------|------|------|------|----------|
| A | lib-a | ... | ... | ... |
| B | lib-b | ... | ... | ... |
| C | lib-c | ... | ... | ... |

请确认使用 A / B / C（或说明其他需求）。
```

---

## 2. Reuse before creating

**Before writing new logic:**

1. **Search the codebase** for:
   - `src/utils/`, `src/helpers/`, `src/lib/` — 通用工具、格式化、校验
   - `src/components/` — 已有 UI 或业务组件
   - `src/hooks/` — 可复用 hooks
   - `src/api/`, `src/services/` — 已有接口封装
2. **If a suitable util/component/hook exists** → use it; do not duplicate.
3. **If similar but not exact** → extend or compose (wrapper component, extra util), then use.
4. **Only create new** when no reusable piece exists or can be reasonably extended.

Briefly note in the implementation what was reused (e.g. "使用 `utils/formatDate`").

---

## 3. UI vs business component split

**Layering rules:**

- **UI (presentational) components**: Pure display and interaction. Receive data and callbacks via props. No direct API calls or global state; no business rules. Place in `src/components/` (e.g. `Button`, `Card`, `FormField`).
- **Business (container) components**: Orchestrate data (API, Zustand), handle business rules, pass data/callbacks to UI components. Place in `src/features/<feature>/` or `src/pages/<page>/` (e.g. `UserListContainer`, `OrderFormContainer`).

**Conventions:**

- One folder per feature or page; inside it split `components/` (UI) and container/hook files (business).
- UI components stay in `src/components/` when shared across features; feature-specific UI can live under `src/features/<name>/components/`.
- Containers/pages import UI components and hooks; UI components do not import from API or store.

**Example structure:**

```
src/
├── components/           # 共享 UI 组件
│   ├── Button/
│   └── Table/
├── features/
│   └── user/
│       ├── components/   # 该 feature 专用 UI
│       │   └── UserAvatar.tsx
│       ├── hooks/
│       │   └── useUserList.ts
│       ├── UserListPage.tsx   # 业务/容器
│       └── api.ts
├── pages/                # 页面级容器，组合 features
└── routes.ts
```

---

## 4. Data-driven routing

**Routes must be defined as data (config), not inline JSX only.**

1. **Define a route config** (e.g. `src/routes.ts` or `src/config/routes.ts`):
   - Array of objects: `path`, `element` (lazy or component reference), `children?`, `meta?` (title, auth, etc.).
2. **Use a single router component** (e.g. in `App.tsx`) that reads this config and renders `<Routes>` / `<Route>` via a small helper or map.
3. **Lazy-load pages** with `React.lazy` + `Suspense` in the config or in the renderer.

**Example shape:**

```ts
// src/routes.ts
export const routeConfig = [
  { path: '/', element: <HomePage />, meta: { title: '首页' } },
  { path: '/users', element: <UsersPage />, meta: { title: '用户' }, children?: [...] },
];
```

Router in App (or dedicated component) maps `routeConfig` to `<Route>` elements. New pages = add entry to config, not scatter `<Route>` across files.

---

## 5. Test-first (red / green)

**Workflow:**

1. **Write or update a test first** that describes the desired behavior (unit or component test). Run tests → **red**.
2. **Implement the minimum code** to make that test pass. Run tests → **green**.
3. **Refactor** if needed; keep tests green.

**Conventions:**

- Use **Vitest** + **jsdom**; place tests next to source (`*.test.ts` / `*.test.tsx`) or in `__tests__/`.
- Test behavior and contracts (props, events), not implementation details.
- For new components: at least one test (render, key interaction or output). For new utils/hooks: unit tests for main branches and edge cases.

---

## 6. React: function components only

- Use **function components** and **hooks**; no class components.
- Prefer `const ComponentName: React.FC<Props> = (props) => { ... }` or plain function with typed props.
- Use hooks for state (`useState`), side effects (`useEffect`), and shared logic (`useCallback`, `useMemo`, custom hooks).

---

## Workflow summary

When generating frontend code for a feature or page:

1. **Reuse**: Search utils, components, hooks, api; use or extend before creating new.
2. **Third-party**: If a new lib is needed, propose 3 options with pros/cons; add only after user confirmation.
3. **Layers**: Implement UI components (presentational) and business/container components (data, API, state) in the right places.
4. **Routes**: Add or extend the route config array; do not scatter `<Route>` definitions.
5. **Test-first**: Write failing test → implement → green → refactor.
6. **React**: Function components and hooks only.
