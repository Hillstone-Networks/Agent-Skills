# 前端代码生成规范参考

用于 React 项目功能/页面/组件开发时查阅。遵循：复用优先、UI 与业务分层、数据化路由、测试先行、函数组件。

## 技术栈默认对齐

| 类别 | 默认 |
|------|------|
| Framework | React（函数组件） |
| UI | Ant Design |
| Router | react-router-dom |
| Language | TypeScript |
| State | Zustand |
| Test | Vitest + jsdom |
| Style | Tailwind CSS |
| HTTP | Axios |
| Build | Vite |

## 1. 第三方库：三选一

引入新依赖时**不得直接安装**。须：(1) 提出恰好 3 个方案；(2) 每方案列出库名、优点、缺点、适用场景；(3) 请用户选择（如「请确认使用选项 A/B/C」）；(4) 仅安装用户确认的依赖，并在 README/AGENTS 中记录。

## 2. 复用优先

写新逻辑前：搜索 `src/utils/`、`src/helpers/`、`src/lib/`、`src/components/`、`src/hooks/`、`src/api/`、`src/services/`。有可复用则用或扩展；仅在没有可复用或无法合理扩展时新建。实现处简要注明复用来源（如「使用 `utils/formatDate`」）。

## 3. UI 与业务组件分层

- **UI（展示）组件**：纯展示与交互，通过 props 接收数据与回调；不直接调 API、不读全局状态；放在 `src/components/`。
- **业务（容器）组件**：组织数据（API、Zustand）、业务规则，将数据/回调传给 UI 组件；放在 `src/features/<feature>/` 或 `src/pages/<page>/`。
- 每 feature/page 一目录，内部分 `components/`（UI）与容器/hook 文件；共享 UI 放在 `src/components/`。

## 4. 数据化路由

路由须以**数据配置**定义，而非仅在 JSX 内联。在 `src/routes.ts` 或 `src/config/routes.ts` 定义数组：`path`、`element`（lazy 或组件引用）、`children?`、`meta?`。用单一路由组件根据该配置渲染 `<Routes>`/`<Route>`。新页面 = 在配置中增加条目，不分散写多处 `<Route>`。

## 5. 测试先行（红/绿）

先写或更新测试描述预期行为 → 运行测试（红）→ 实现最小代码使通过（绿）→ 必要时重构并保持绿。使用 Vitest + jsdom；测试贴源 `*.test.{ts,tsx}` 或 `__tests__/`。测行为与契约（props、事件），不测实现细节。

## 6. React：仅函数组件

使用函数组件与 hooks；不用类组件。推荐 `const ComponentName: React.FC<Props> = (props) => { ... }` 或带类型 props 的普通函数。

## 流程小结

1. 复用：先查 utils、components、hooks、api，再用或扩展。2. 第三方：新库须三方案、用户选后再装。3. 分层：UI 组件与业务/容器组件分目录。4. 路由：维护路由配置数组，不散落 `<Route>`。5. 测试先行：先红后绿再重构。6. 仅函数组件与 hooks。
