---
name: cicd-fullstack-flask-react
description: When user asks to set up CI/CD for a Flask + React fullstack project: detect or ask for frontend and backend directories, generate CI/CD files, then check backend and add static/SPA serving if missing. Use when the user wants CI/CD for fullstack, or to fix backend not serving frontend build.
---

# CI/CD Fullstack Flask + React

**Scope**: When the user **invokes this skill**, work in **the user's project** (the codebase they are in). Do not modify the repository that only *contains* this skill file; only change the project the user is asking to set up.

---

## Workflow (Do in Order)

### Step 1: Determine the frontend and backend directories

- **Frontend directory**  
  List the **user's project root**: look for a subdirectory that is the frontend (contains `package.json`). Common names: `frontend`, `web`, `client`, `fe`, `ui`.  
  - If exactly one such directory → use it as `<frontend_dir>`.  
  - If none or multiple, or unclear → **Ask the user**: “前端目录是哪个？请告知文件夹名（如 frontend / web / client）。” Use the user's answer as `<frontend_dir>`.

- **Backend directory**  
  Look for the backend: a subdirectory that contains `requirements.txt` or the Flask app (e.g. `app/__init__.py`, `wsgi.py`), or the repo root if the app and `requirements.txt` are at root. Common names: `app`, `backend`, `server`, `api`; sometimes backend is repo root (`.`).  
  - If exactly one clear candidate → use it as `<backend_dir>`.  
  - If none or multiple, or unclear → **Ask the user**: “后端目录是哪个？请告知文件夹名（如 app / backend / server，或根目录）。” Use the user's answer as `<backend_dir>`.

- Do not guess; use the same names everywhere (CI/CD, Dockerfile, and backend code).

### Step 2: Generate or adapt CI/CD files

- Using `<frontend_dir>` and `<backend_dir>`:
  - **Root `.gitlab-ci.yml`** (if needed): build stage that builds Docker image; Dockerfile must reference both dirs. Deploy stages as needed (e.g. push_image, dev_deploy, prod_deploy).
  - **Dockerfile**:  
    - Stage 1 (frontend): `WORKDIR /<frontend_dir>`, `COPY <frontend_dir>/`, `npm run build`.  
    - Final stage: copy backend (e.g. `COPY . /app/` with context so `<backend_dir>` content is at `/app`, or `COPY <backend_dir>/ /app/` if backend is a subdir) + `COPY --from=frontend-builder /<frontend_dir>/dist /app/<frontend_dir>/dist`.  
    - Ensure `WORKDIR` and entrypoint (e.g. `run.sh`) match `<backend_dir>` layout (if backend is subdir `backend/`, copy to `/app` and run from there).
  - **Frontend-only CI** (if frontend has its own `.gitlab-ci.yml` under `<frontend_dir>/`): build in that folder, publish `dist/` (paths relative to that dir).
- Use the **same** `<frontend_dir>` and `<backend_dir>` everywhere; no hardcoded `frontend` or `app` when the project uses different names.

### Step 3: Check whether the backend serves the frontend static files

- In the **user's backend** under `<backend_dir>` (e.g. Flask `create_app()` or main app file), search for:
  - `static_folder` or `static_url_path` pointing to a directory (e.g. `<something>/dist`).
  - A catch-all route that returns `index.html` (or equivalent) for SPA.
- If both exist and the path clearly points to the frontend build output (e.g. `.../frontend/dist` or `.../web/dist`) → **nothing to do** for this step.

### Step 4: If the backend does NOT serve the frontend build → add it

- **Do not** change the user's project to use environment variables for the frontend path. Use the **already known** `<frontend_dir>` from Step 1 (detected or user answer).
- In the Flask app factory (or equivalent) under `<backend_dir>`:
  1. Set `static_dir = os.path.join(repo_root, '<frontend_dir>', 'dist')`. `repo_root` is the project root (e.g. one or two levels up from the file, depending on whether `<backend_dir>` is `app` or `backend` with `app` inside).
  2. Create the app with `static_folder=static_dir`, `static_url_path=''`.
  3. **After** all API/blueprint registration, add a catch-all route that: if the path exists as a file under `static_dir`, serve it; otherwise serve `index.html`.
- Use the actual `<frontend_dir>` and `<backend_dir>` from Step 1. Example (replace with real names, e.g. `frontend`/`web`, `app`/`backend`):

```python
# In create_app() under <backend_dir>; repo_root = parent of <backend_dir> (or same as <backend_dir> if backend is root)
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))   # if file is <backend_dir>/app/__init__.py
# or _root = os.path.dirname(os.path.abspath(__file__))  # if backend is repo root
static_dir = os.path.join(_root, '<frontend_dir>', 'dist')
flask_app = Flask(__name__, static_folder=static_dir, static_url_path='')
# ... register APIs ...
@flask_app.route('/', defaults={'path': ''})
@flask_app.route('/<path:path>')
def serve_spa(path):
    if path and os.path.exists(os.path.join(flask_app.static_folder, path)):
        return send_from_directory(flask_app.static_folder, path)
    return send_from_directory(flask_app.static_folder, 'index.html')
```

### Step 5: Frontend routing (when backend serves SPA)

- If the backend will serve the SPA (single `index.html` for all non-API paths), the frontend should use **hash routing** so the server does not need to know every route.
- In the user's frontend router: if you see `createBrowserRouter` or `BrowserRouter`, replace with `createHashRouter`; routes config can stay the same.

---

## CI/CD Reference (for generating files)

- **Root repo**: stages e.g. build → deploy; build Docker image (with frontend built in Dockerfile); push_image; dev_deploy / prod_deploy by branch.
- **Dockerfile**: Node stage `WORKDIR /<frontend_dir>`, `COPY <frontend_dir>/`, `npm run build`; final stage copy backend (from `<backend_dir>`) and `/<frontend_dir>/dist` to `/app/...` so paths match what the app expects.
- **Frontend-only pipeline** (optional): under `<frontend_dir>/`, build + publish `dist/` to nginx or static host.

---

## Summary

1. Inspect user's project → get `<frontend_dir>` and `<backend_dir>` (or ask user for either if uncertain).
2. Generate/adapt CI/CD so all references use `<frontend_dir>` and `<backend_dir>`.
3. In `<backend_dir>`, check: does the app already serve `<frontend_dir>/dist` and `index.html`?
4. If not → add static_folder + SPA fallback using `<frontend_dir>`; path from backend to repo root depends on `<backend_dir>`.
5. If backend serves SPA → ensure frontend uses hash router.
