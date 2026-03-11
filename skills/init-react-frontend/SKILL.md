---
name: init-react-frontend
description: "Scaffolds a new React frontend with Vite (Rolldown), React Compiler, TypeScript, Ant Design, react-router, Zustand, Vitest, jsdom, Tailwind CSS, Axios. Uses create-vite in Rolldown form with React + Compiler + TS by default. Creates utils, consts, route, components, test directories (route separate from consts). All dependencies use latest versions. Use when initializing a frontend project or setting up React + TypeScript + Vite stack."
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
| Test      | Vitest + jsdom                           |
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
| `test/` or `src/test/` | Test-related: Vitest global setup, fixtures, mocks, e2e; unit tests can still live next to source as `**/*.test.{ts,tsx}` |

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
| `src/**/*.test.tsx` | At least one example test |
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

## Reference

- **AGENTS template:** `assets/templates/AGENTS.template.md` — fill placeholders for the new project’s name, stack, structure, and scripts.
