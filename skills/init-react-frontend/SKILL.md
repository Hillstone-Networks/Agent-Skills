---
name: init-react-frontend
description: "Scaffolds a new React frontend with Vite (Rolldown), React Compiler, TypeScript, Ant Design, react-router, Zustand, Vitest, jsdom, Tailwind CSS, Axios. Uses create-vite in Rolldown form with React + Compiler + TS by default. Creates utils, consts, route, components, test directories (route separate from consts); includes unit/component tests and end-to-end (e2e) testing. Optional CI/CD: defaults to GitLab CI, frontend built as nginx Docker image. All dependencies use latest versions. Use when initializing a frontend project or setting up React + TypeScript + Vite stack."
---

# Init React Frontend

Scaffolds a production-ready React frontend with a fixed default stack. Uses the **official Vite scaffold** in **Rolldown** form, defaulting to **React + Compiler + TypeScript**; generates project structure, configs, and a project-specific AGENTS.md.

## Initialization: Vite scaffold + Rolldown

Use the official Vite scaffold to create the project in Rolldown form, defaulting to **React + Compiler + TypeScript**:

1. **Recommended:** Run `npm create vite@latest` (or `pnpm create vite`, `yarn create vite`) in the target directory. If the current create-vite supports choosing the bundler, select **Rolldown**, template **React**, language **TypeScript**; if it offers a React Compiler option, enable it.
2. **If Rolldown is not offered:** Create with `npm create vite@latest <project-name> -- --template react-ts`, then in `package.json` devDependencies set `"vite": "npm:rolldown-vite@<resolved-latest-version>"`, and enable React Compiler in the Vite config (see tech stack and file checklist below).

When generating or filling in files, ensure the build uses Rolldown (`rolldown-vite`) and React Compiler is enabled by default.

## Default tech stack (when not specified)

| Category   | Default choice                          |
|-----------|------------------------------------------|
| Framework | React                                    |
| Compiler  | React Compiler (enabled in Vite)         |
| UI        | Ant Design                               |
| Router    | react-router (react-router-dom)          |
| Language  | TypeScript                               |
| State     | Zustand                                  |
| Test      | Vitest + jsdom（单元/组件）；端到端测试（e2e） |
| Style     | Tailwind CSS                             |
| HTTP      | Axios                                    |
| Build     | Vite + Rolldown (via `rolldown-vite`)    |

If the user specifies a different stack (e.g. Vue, different UI lib), use their choices; use the table above for any unspecified category.

## Required directory structure

Create the following directories under `src/` at initialization (optionally with placeholder files such as `.gitkeep` or a short README describing purpose):

| Directory            | Purpose |
|----------------------|---------|
| `src/utils/`        | Utility functions (helpers, formatting, generic pure functions) |
| `src/consts/`       | Constants (API URLs, enums, config constants; **not** routes — see `src/route/`) |
| `src/route/`        | Routing: route config, path constants, route table (separate from consts) |
| `src/components/`   | Shared UI components (reusable components decoupled from business pages) |
| `test/` or `src/test/` | Test-related: Vitest global setup, fixtures, mocks, **e2e 目录与用例**；单元测试可放在源码旁 `**/*.test.{ts,tsx}`。需同时包含端到端测试（e2e）能力与示例。 |

Also keep the skill defaults: `src/pages/`, `src/store/`, `src/api/` or `src/services/`. When generating AGENTS.md, `{{DIR_STRUCTURE}}` must include the above directory descriptions.

## Dependency version strategy

**All** third-party dependencies (including libraries added later to the project) must use **the latest stable version at the time the skill runs**. Do not hardcode older versions.

1. **Resolve versions when generating:** Before writing `package.json`, query the registry for the latest version of each dependency, e.g. `npm view react version`, `npm view vite version`, `npm view rolldown-vite version`, and for antd, react-router-dom, zustand, vitest, jsdom, tailwindcss, axios, React Compiler–related packages and their peer/typed deps.
2. **Write exact versions** in `package.json` (no `^`/`~` or `latest`) so the generated project is reproducible.
3. **When adding libraries later:** For any new third-party library, use the latest stable version at that time (e.g. `npm view <pkg> version`) and write the exact version.
4. Document in the project README or AGENTS.md that dependency versions were resolved at scaffold time and that the user can upgrade later.

## Workflow

### 1. Gather project info

- **Project name and one-line description** — Used in README and AGENTS.md.
- **Tech stack** — If the user does not specify, use the default stack above. If they replace only some items (e.g. “use Vue”), keep defaults for the rest.
- **Backend dev port (if there is a backend or full-stack setup)** — Used to configure the dev proxy target; default **5000**; confirm against the backend project’s actual listen port (e.g. backend README, AGENTS.md, or startup script `port`).
- **是否生成 CI/CD** — 若用户要求生成 CI/CD，默认生成 **GitLab CI** 配置，并将前端打包为 **nginx 镜像**（见下文「CI/CD」）；若用户指定其他 CI（如 GitHub Actions），则按用户选择生成。
- **Documentation language** — Default: English. Use another language if the user asks.

### 2. Resolve dependency versions

Run version resolution for every package that will appear in `package.json` (see “Dependency version strategy”). Use the resolved versions in the next step.

### 3. Generate project files

Create the project in the target directory (current folder or path given by the user).

**File checklist:**

| Path / area | Purpose |
|-------------|--------|
| `package.json` | Scripts: `dev`, `build`, `preview`, `test`; all deps at resolved latest exact versions; Vite via Rolldown: `"vite": "npm:rolldown-vite@<version>"` in devDependencies |
| `vite.config.ts` | Vite config: React plugin, React Compiler enabled, path alias (e.g. `@/` → `src/`), build output; **dev proxy:** `server.proxy` to forward API requests (e.g. `/api`) to backend, default target port **5000**, confirm against backend’s actual port |
| `tsconfig.json` / `tsconfig.node.json` | TypeScript config for app and Vite |
| `tailwind.config.js` + `postcss.config.js` | Tailwind 3+ and PostCSS |
| `index.html` | Root HTML; script entry to `src/main.tsx` |
| `src/main.tsx` | React root entry, Ant Design style import, mount |
| `src/App.tsx` | Root component: react-router `BrowserRouter` and minimal route list |
| `src/App.css` | Optional global styles; include Tailwind directives if used |
| `src/utils/` | Utils directory (see “Required directory structure” above) |
| `src/consts/` | Constants (API URLs, enums, etc.; do not put routes here) |
| `src/route/` | Route directory (route config, paths, route table) |
| `src/components/` | Shared components directory |
| `src/pages/` | Placeholder pages (e.g. Home) for routes |
| `src/store/` | Optional Zustand store example |
| `src/api/` or `src/services/` | Axios instance or placeholder |
| `test/` or `src/test/` | Test directory: setup, fixtures, mocks |
| `vitest.config.ts` | Vitest + jsdom; match `**/*.test.{ts,tsx}` |
| `src/**/*.test.tsx` | At least one example unit/component test |
| **e2e**（如 `test/e2e/` 或 `e2e/`） | 端到端测试：配置与至少一条 e2e 用例（可选工具：Playwright、Cypress 等，按项目选型）；`package.json` 中需有 `test:e2e` 等脚本 |
| `.gitignore` | Node, dist, env, IDE |
| `AGENTS.md` | From template below; filled for this project |

**Rolldown:** In `package.json` devDependencies set `"vite": "npm:rolldown-vite@<resolved-version>"`; keep scripts `vite` / `vite build` / `vite preview`; no extra config. **React Compiler:** Enable in the Vite React plugin config (per current @vitejs/plugin-react and rolldown-vite docs).

**Dev proxy:** After the backend project is initialized, configure the dev proxy in `vite.config.ts` under `server.proxy` (e.g. proxy `/api` to `http://localhost:<backend-port>`). Default backend port is **5000**; confirm against the backend’s actual listen port (backend README, AGENTS.md, or startup config). If there is no backend yet, use 5000 or comment out the proxy and update when the backend is ready.

### 4. AGENTS.md for the generated project

Generate `AGENTS.md` at the **project root** of the scaffolded app (not this skill repo). Use the template in `assets/templates/AGENTS.template.md`.

**Placeholders:**

- `{{PROJECT_NAME}}` — Project name
- `{{PROJECT_DESCRIPTION}}` — One-line description
- `{{TECH_STACK_TABLE}}` — Tech stack table matching the chosen stack (default or user overrides)
- `{{DIR_STRUCTURE}}` — Directory tree of the generated app; must include `src/utils/`, `src/consts/`, `src/route/`, `src/components/`, `test/` or `src/test/`, plus `src/pages/`, `src/store/`, config files
- `{{SCRIPTS}}` — `dev`, `build`, `preview`, `test` and what they do
- `{{INITIALIZED_DATE}}` — Date in `YYYY-MM-DD`

Keep AGENTS.md aligned with the actual stack, scripts, and layout. Language: same as chosen for the project (default English).

### 5. Post-generation

- Run `npm install` (or the chosen package manager) in the project root.
- **Install frontend-codegen skill** so the new project can use it for generating pages/components/features. Run in the project root (or the workspace where the user will develop):  
  `npx skills add Hillstone-Networks/Agent-Skills -s frontend-codegen`  
  If the user’s environment uses a different skills repo or agent, use the equivalent command to add the `frontend-codegen` skill.
- Optionally run `npm run build` and `npm run test` to verify.
- Tell the user the project is ready, that **frontend-codegen** is installed for code generation, and where AGENTS.md and key configs live.

### 6. CI/CD（当用户要求生成时）

若用户要求生成 CI/CD 配置，则**默认使用 GitLab CI**，并将前端构建产物打包为 **nginx 镜像**：

1. **GitLab CI 默认**：在项目根目录生成 `.gitlab-ci.yml`（或用户指定的 GitLab CI 配置路径）。流水线至少包含：依赖安装、lint、单元/组件测试、构建、以及构建 Docker 镜像并推送（若用户需要）。
2. **前端 nginx 镜像**：构建阶段产出 `dist/`（或 Vite 配置的 `build.outDir`）后，使用 **nginx 镜像** 作为运行环境：
   - 提供 `Dockerfile`（或多阶段 Dockerfile）：以合适版本的 nginx 基础镜像（如 `nginx:alpine`），将 `dist/` 拷贝到 nginx 静态目录（如 `/usr/share/nginx/html`），并可按需提供默认 nginx 配置（如 SPA fallback、gzip 等）。
   - GitLab CI 中“构建镜像”的 job 使用该 Dockerfile，将前端打包成可部署的 nginx 镜像；若用户需要推送到镜像仓库，在 `.gitlab-ci.yml` 中配置登录与 push 步骤。
3. 若用户明确要求 GitHub Actions 或其他 CI，则按用户选择生成对应配置；未指定时默认 GitLab CI + nginx 镜像。

## Reference

- **AGENTS template:** `assets/templates/AGENTS.template.md` — fill placeholders for the new project’s name, stack, structure, and scripts.
