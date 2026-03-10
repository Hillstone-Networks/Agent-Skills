---
name: init-react-frontend
description: "Scaffolds a new React frontend with Vite, TypeScript, Ant Design, react-router, Zustand, Vitest, jsdom, Tailwind CSS, Axios, and Rolldown. Generates package.json with latest dependency versions, Vite config, and project-specific AGENTS.md. Use when the user wants to initialize a frontend project, create a new React app, or set up a React + TypeScript + Vite stack."
---

# Init React Frontend

Scaffolds a production-ready React frontend with a fixed default stack. Generates project structure, configs, and an AGENTS.md tailored to the created project.

## Default tech stack (when not specified)

| Category   | Default choice                          |
|-----------|------------------------------------------|
| Framework | React                                    |
| UI        | Ant Design                               |
| Router    | react-router (react-router-dom)          |
| Language  | TypeScript                               |
| State     | Zustand                                  |
| Test      | Vitest + jsdom                           |
| Style     | Tailwind CSS                             |
| HTTP      | Axios                                    |
| Build     | Vite + Rolldown (via `rolldown-vite`)    |

If the user specifies a different stack (e.g. Vue, different UI lib), use their choices; for any unspecified category, use the default above.

## Dependency version strategy

All third-party dependencies must use **the latest stable version at the time the skill runs**. Do not hardcode old versions.

1. **Resolve versions when generating**: Before writing `package.json`, query the registry for each dependency, e.g.:
   - `npm view react version`
   - `npm view vite version`
   - (repeat for antd, react-router-dom, zustand, vitest, jsdom, tailwindcss, axios, rolldown-vite, and their peer/typed deps)
2. **Write exact versions** into `package.json` (no `^`/`~` or `latest`) so the generated project is reproducible.
3. Document in the project README or AGENTS.md that versions were chosen at scaffold time and that the user can upgrade later.

## Workflow

### 1. Gather project info

- **Project name and one-line description** — Used in README and AGENTS.md.
- **Tech stack** — If the user does not specify, use the default stack above. If they replace only some items (e.g. “use Vue”), keep defaults for the rest.
- **Documentation language** — Default: 中文. Switch to English or another language if the user asks.

### 2. Resolve dependency versions

Run version resolution for every package that will appear in `package.json` (see “Dependency version strategy”). Use the resolved versions in the next step.

### 3. Generate project files

Create the project in the target directory (current folder or path given by the user).

**File checklist:**

| Path / area | Purpose |
|-------------|--------|
| `package.json` | Scripts: `dev`, `build`, `preview`, `test`; all deps with resolved latest versions; Vite + Rolldown via `"vite": "npm:rolldown-vite@<version>"` in devDependencies |
| `vite.config.ts` | Vite config: React plugin, path alias (e.g. `@/` → `src/`), build output |
| `tsconfig.json` / `tsconfig.node.json` | TypeScript for app and Vite |
| `tailwind.config.js` + `postcss.config.js` | Tailwind 3+ and PostCSS |
| `index.html` | Root HTML; script entry to `src/main.tsx` |
| `src/main.tsx` | React root, Ant Design style import, mount |
| `src/App.tsx` | Root component with react-router `BrowserRouter` and a minimal route list |
| `src/App.css` | Optional global styles; ensure Tailwind directives if used |
| `src/pages/` | Placeholder pages (e.g. Home) used by routes |
| `src/store/` | Optional Zustand store example |
| `src/api/` or `src/services/` | Axios instance or placeholder |
| `vitest.config.ts` | Vitest + jsdom; test match pattern (e.g. `**/*.test.{ts,tsx}`) |
| `src/**/*.test.tsx` | At least one example test |
| `.gitignore` | Node, dist, env, IDE |
| `AGENTS.md` | From template below; filled for this project |

**Rolldown:** In `package.json`, set Vite to the Rolldown build:  
`"vite": "npm:rolldown-vite@<resolved-version>"` in `devDependencies`, and use standard Vite scripts (`vite`, `vite build`, `vite preview`). No extra config required.

### 4. AGENTS.md for the generated project

Generate `AGENTS.md` at the **project root** of the scaffolded app (not this skill repo). Use the template in `assets/templates/AGENTS.template.md`.

**Placeholders:**

- `{{PROJECT_NAME}}` — Project name
- `{{PROJECT_DESCRIPTION}}` — One-line description
- `{{TECH_STACK_TABLE}}` — Tech stack table matching the chosen stack (default or user overrides)
- `{{DIR_STRUCTURE}}` — Directory tree of the generated app (e.g. `src/`, `src/pages/`, `src/store/`, config files)
- `{{SCRIPTS}}` — `dev`, `build`, `preview`, `test` and what they do
- `{{INITIALIZED_DATE}}` — Date in `YYYY-MM-DD`

Keep AGENTS.md aligned with the actual stack, scripts, and layout. Language: same as chosen for the project (default 中文).

### 5. Post-generation

- Run `npm install` (or the package manager chosen) in the project root.
- **Install frontend-codegen skill** so the new project can use it for generating pages/components/features. Run in the project root (or the workspace where the user will develop):  
  `npx skills add Hillstone-Networks/Agent-Skills -s frontend-codegen`  
  If the user’s environment uses a different skills repo or agent, use the equivalent command to add the `frontend-codegen` skill.
- Optionally run `npm run build` and `npm run test` to verify.
- Tell the user the project is ready, that **frontend-codegen** is installed for code generation, and where AGENTS.md and key configs live.

## Reference

- **AGENTS template:** `assets/templates/AGENTS.template.md` — fill placeholders for the new project’s name, stack, structure, and scripts.
