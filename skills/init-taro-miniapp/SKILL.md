---
name: init-taro-miniapp
description: "Scaffolds a Taro mini-program project using npx @tarojs/cli init <projectName> (e.g. npx @tarojs/cli init myApp), standard component library @tarojs/components per Taro docs, and generates project-specific AGENTS.md with code-gen rules (reuse-first, unified style, third-party options, UI/business separation). Use when initializing a mini-program, Taro project, or multi-end (weapp/h5/rn) app."
---

# Init Taro Mini-Program

Scaffold a cross-platform mini-program with the latest Taro, follow the official component library conventions, and generate an AGENTS.md with code-generation constraints.

## Reference Docs

- [Taro Introduction & Installation](https://docs.taro.zone/docs/)
- [Installation & Usage](https://docs.taro.zone/docs/GETTING-STARTED)
- [Component Library](https://docs.taro.zone/docs/components-desc) — Use `@tarojs/components`; event props start with `on`, component names are PascalCase.

## Default Tech Stack (when unspecified)

| Category   | Default choice                          |
|------------|-----------------------------------------|
| Framework  | Taro (latest stable)                    |
| Syntax     | React or Vue3 (selectable during init)  |
| Language   | TypeScript                              |
| Components | @tarojs/components (Taro standard)      |
| UI extras  | Optional taro-ui@next (Taro 3+)         |

If the user specifies another framework (e.g. Vue3, Preact), use that; otherwise React + TypeScript is the default.

## Dependency Version Strategy

- Use the latest Taro versions when initializing the project.
- Before generating, you may check: `npm info @tarojs/cli version`, `npm info @tarojs/taro version`, etc.
- Write pinned versions in `package.json` (e.g. with `^` for upgrades) and note in README or AGENTS.md that versions were chosen at scaffold time.

## Workflow

### 1. Gather project info

- **Project name and short description** — For README and AGENTS.md.
- **Framework and syntax** — React / Vue3 / Preact, and whether to use TypeScript.
- **Target platforms** — WeChat mini-program, H5, multi-end, etc. (affects scripts and config).
- **Doc language** — Default is English (or match project preference).

### 2. Initialize with latest Taro

From the target directory, run (use npx so the latest CLI is used):

```bash
npx @tarojs/cli init <projectName>
```

Example when the project name is `myApp`:

```bash
npx @tarojs/cli init myApp
```

- During init, choose as needed: framework (React/Vue3 etc.), TypeScript, CSS preprocessor, bundler, package manager.
- If initializing inside an existing directory, use the current directory name as the project name or create a subdirectory first, then run init.
- If `@tarojs/cli` is installed globally, `taro init <projectName>` is also valid, but prefer the npx form above.

### 3. Create common business directories

Under the project **src**, add directories for organizing code by responsibility (keep or extend any that Taro already created):

- **apis** — API wrappers and request helpers
- **utils** — Utilities
- **components** — Shared and feature components
- **consts** — Constants, enums, config
- Optional: **hooks** (for React), **services** (business services)

Add others as needed (e.g. `types`, `stores`) and reflect them in AGENTS.md’s `{{DIR_STRUCTURE}}`.

### 4. Install dependencies

After init and directory setup, from the **project root** run:

```bash
npm install
```

(Use pnpm or yarn if that was chosen during init.) Ensure dependencies are installed before configuring proxy and running scripts.

### 5. Configure dev proxy for backend

Add a dev proxy in the project config so the frontend can talk to the backend during local development and avoid CORS. By default assume the backend runs on port **5000**.

- Config file: usually `config/index.js` (or `config/dev.js`, depending on the project).
- Under **h5** → **devServer**, add **proxy** to forward `/api` (or your chosen prefix) to the backend, e.g.:

```javascript
h5: {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',  // default 5000; change to backend port if different
        changeOrigin: true,
        pathRewrite: { '^/api': '/api' }  // adjust to match backend routes
      }
    }
  }
}
```

- If the backend port is not 5000, set `target` to `http://localhost:<port>`. If the backend has a path prefix, adjust `pathRewrite` accordingly.
- Mini-program targets have no devServer; in WeChat DevTools → Details → Local settings, enable “Do not verify legal domain” for device/simulator debugging, or configure valid request domains. For H5, use the proxy above to reach the backend.

Document in AGENTS.md or README: the proxy prefix (e.g. `/api`) and backend port (default 5000) for local H5 development.

### 6. Component library (@tarojs/components)

- Follow the [Taro component docs](https://docs.taro.zone/docs/components-desc); import from `@tarojs/components`.
- React example:

```tsx
import { View, Text } from '@tarojs/components'
```

- Conventions:
  - Component names **PascalCase** (e.g. `Map`, `View`).
  - Event props start with **on** (e.g. `onClick`, `onTap`), matching mini-program `bind` usage.
- Optional: [Taro UI](https://taro-ui.jd.com/) for multi-end UI (Taro 3+ use `taro-ui@next`).

### 7. Generate AGENTS.md

In the **initialized project root**, generate `AGENTS.md` from this skill’s `assets/templates/AGENTS.template.md`.

**Placeholders:**

- `{{PROJECT_NAME}}` — Project name
- `{{PROJECT_DESCRIPTION}}` — Short description
- `{{TECH_STACK_TABLE}}` — Tech stack table (Taro, React/Vue, TS, @tarojs/components, etc.)
- `{{DIR_STRUCTURE}}` — Directory tree (including `src/` with apis, utils, components, consts, and `config/`, `dist/`)
- `{{SCRIPTS}}` — Common scripts (e.g. `dev:weapp`, `build:weapp`, `dev:h5`, `build:h5`) and their purpose
- `{{INITIALIZED_DATE}}` — Init date in `YYYY-MM-DD`

Use the project’s chosen doc language (default English).

### 8. Code-generation rules (in AGENTS.md)

The generated AGENTS.md must include these rules (the template already has them; keep them after filling):

- **a. Reuse first** — Before adding code, look in `utils`, `components`, `hooks`, `api`; reuse or extend instead of duplicating.
- **b. Consistent style** — Follow existing project style (naming, indentation, quotes, component patterns).
- **c. New third-party libs** — Propose at least 2–3 options with pros/cons; install and document only after the user chooses.
- **d. Separate UI and business** — Split presentational/interactive components from data, APIs, and state; containers/pages own business logic; pure UI components only receive props and callbacks.

### 9. Next steps

- Dependencies are installed in step 4; optionally run `npm install` again to confirm.
- Optional: run `npm run dev:weapp` (or `dev:h5` for the target platform) and open `dist` in the dev tools; for H5, verify the proxy works.
- Tell the user the project is ready, where AGENTS.md is, the directory conventions (apis, utils, components, consts, etc.), and the backend proxy (default port 5000).

## Template paths

- **AGENTS template:** `assets/templates/AGENTS.template.md` — Fill with the placeholders above (project name, tech stack, dir structure, scripts, date).
