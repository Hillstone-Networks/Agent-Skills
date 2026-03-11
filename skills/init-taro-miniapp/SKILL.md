---
name: init-taro-miniapp
description: "Initializes a Taro mini-program with npx @tarojs/cli init <projectName>; after init requires npm install, then creates directories under src, configures dev proxy for API, and may add/update README and AGENTS.md. No other file or config changes. Use when scaffolding a Taro/mini-program project."
---

# Init Taro Mini-Program

Initialize a Taro project **only** with the official CLI; after init, create directories, configure the API proxy, and may add or update README and AGENTS.md. Do not modify any other generated files or config.

## Constraint

- **Init command (mandatory):** Must use `npx @tarojs/cli init <projectName>` to create the project. Do not use global `taro init` or other scaffolding.
- **Required after init:** Run `npm install` (or `pnpm install` / `yarn` if chosen during init) from the project root; do not skip.
- **After init (allowed only):** (1) create new directories under `src`, (2) add or edit the dev proxy configuration for the backend API, and (3) add or edit README and AGENTS.md. Do **not** change `package.json`, existing source files, or other config files.

## Reference Docs

- [Taro Introduction & Installation](https://docs.taro.zone/docs/)
- [Installation & Usage](https://docs.taro.zone/docs/GETTING-STARTED)

## Workflow

### 1. Initialize with Taro CLI (required)

From the parent directory where the project should be created, run:

```bash
npx @tarojs/cli init <projectName>
```

Example:

```bash
npx @tarojs/cli init myApp
```

- Use **only** this command to create the project. During the interactive init, the user (or you on their behalf) may choose framework (React/Vue3), TypeScript, CSS preprocessor, bundler, package manager.
- Do not replace or re-scaffold with any other tool or template.

### 2. Install dependencies (required)

From the **project root** (the directory created by init), run:

```bash
npm install
```

If the user chose pnpm or yarn during init, use `pnpm install` or `yarn` instead. This step is **required**; do not skip it.

### 3. Create directories under `src`

Only add these directories under the project's **src** (create only if missing; do not change existing files):

- **apis** — API wrappers and request helpers
- **utils** — Utilities
- **components** — Shared and feature components
- **consts** — Constants, enums, config

Optionally add: **hooks** (React), **services**. Do not add files inside them unless the user explicitly asks; creating empty directories is enough.

### 4. Configure dev proxy for API

Only modify the project config to add the H5 dev proxy so the frontend can call the backend during local development. Default backend port: **5000**.

- Config file: usually `config/index.js` (or `config/dev.js` in the generated project).
- Under **h5** → **devServer**, add or merge **proxy** (e.g. forward `/api` to the backend):

```javascript
h5: {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        pathRewrite: { '^/api': '/api' }
      }
    }
  }
}
```

- If the backend port is not 5000, set `target` to `http://localhost:<port>`. Adjust `pathRewrite` if the backend uses a different path prefix.
- Do not change other options in the config file beyond what is needed for this proxy.

### 5. Add or update README and AGENTS.md

- **AGENTS.md:** In the project root, create or overwrite `AGENTS.md` from this skill's template `assets/templates/AGENTS.template.md`. Fill placeholders: `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{TECH_STACK_TABLE}}`, `{{DIR_STRUCTURE}}` (include `src/` with apis, utils, components, consts, and `config/`, `dist/`), `{{SCRIPTS}}`, `{{INITIALIZED_DATE}}` (YYYY-MM-DD).
- **README:** May add or update a project README (e.g. project name, how to run, proxy/port note). Keep minimal unless the user asks for more.

### 6. Do not do

- Do not change `package.json`, dependencies, or scripts (except running the install command in step 2).
- Do not modify existing source files, app entry, or other config (e.g. `app.config.ts`, `babel.config.js`) except the proxy block in step 4.
