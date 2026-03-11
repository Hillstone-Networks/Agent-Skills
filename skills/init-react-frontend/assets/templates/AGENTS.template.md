# AGENTS.md — {{PROJECT_NAME}}

> This file provides shared context for AI assistants working in this project. Keep it accurate and update it as the project evolves. Only append; do not remove existing content without team agreement.

---

## Project overview

**Name:** {{PROJECT_NAME}}  
**Description:** {{PROJECT_DESCRIPTION}}  
**Type:** Frontend application

---

## Tech stack and resources

{{TECH_STACK_TABLE}}

---

## Repository / directory structure

```
{{DIR_STRUCTURE}}
```

- Entry: `index.html` → `src/main.tsx`
- Root component: `src/App.tsx`; routing: `src/route/` (route config, paths, route table)
- Pages: `src/pages/`
- Utils: `src/utils/` (shared utility functions)
- Constants: `src/consts/` (API URLs, enums, etc.; routes live in `src/route/`, not here)
- Shared components: `src/components/`
- State: `src/store/` (Zustand)
- HTTP: `src/api/` or `src/services/` (Axios)
- Tests: Vitest; test dir `test/` or `src/test/` (setup, fixtures, mocks); unit tests next to source as `src/**/*.test.{ts,tsx}`

**Dev proxy:** In `vite.config.ts`, `server.proxy` forwards API requests (e.g. `/api`) to the backend; default target port **5000** — should match the backend’s actual listen port (confirm and update after the backend is initialized).

---

## Development and maintenance

### Scripts

{{SCRIPTS}}

### Code and conventions

- Use TypeScript and follow existing project style
- Organize components and pages under `src/` by feature
- **Feature/page/component work:** Prefer the **frontend-codegen** skill (if installed: `frontend-codegen` from `Hillstone-Networks/Agent-Skills`) for reuse-first, UI/business separation, data-driven routes, test-first, and function components
- When adding capabilities, update this AGENTS.md (e.g. append to “Agent memory log”)

### Test and build

- Unit/component tests: `npm run test` (Vitest + jsdom)
- Production build: `npm run build`; output in `dist/`
- Preview build locally: `npm run preview`

### Documentation language

- Repo-level docs and AGENTS.md default to English; use another language if the team agrees.

---

## Agent memory log

<!-- Append decisions or findings here, format: - [YYYY-MM-DD] content -->
<!-- Initialized {{INITIALIZED_DATE}} -->
