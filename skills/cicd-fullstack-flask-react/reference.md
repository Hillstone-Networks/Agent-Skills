# Reference: Folder Detection and Backend Static Serving

## Finding the frontend directory (Step 1)

- Scan **user's project root** for direct subdirs that contain `package.json`. Those are candidates.
- Common names: `frontend`, `web`, `client`, `fe`, `ui`.
- **If uncertain** (0 or multiple candidates, or repo layout unusual): **Ask the user** for the frontend folder name. Do not guess; do not use env vars.

## Finding the backend directory (Step 1)

- Backend is either the **repo root** (if `requirements.txt` and app code like `app/` are at root) or a **subdir** that contains `requirements.txt` or the Flask app (e.g. `app/__init__.py`, `wsgi.py`).
- Common subdir names: `app`, `backend`, `server`, `api`.
- **If uncertain** (e.g. both root and a subdir look like backend, or multiple subdirs): **Ask the user**: “后端目录是哪个？请告知文件夹名（如 app / backend / server，或根目录）.” Do not guess.

## Backend: how to tell if it already serves the frontend

- Search for `static_folder`, `send_from_directory`, and routes that serve `index.html`.
- If `static_folder` points to a path ending in `dist` (or `build`) and a catch-all returns `index.html`, the backend likely already serves the SPA. Confirm the path matches `<frontend_dir>/dist` (e.g. `.../frontend/dist` or `.../web/dist`).

## Backend: what to add if not serving

- Set `static_folder` to `os.path.join(repo_root, '<frontend_dir>', 'dist')`. `repo_root` is the project root: if `<backend_dir>` is a subdir (e.g. `backend`), go up from the app file; if backend is repo root, repo_root is the same as backend root.
- Register the catch-all **after** all API routes so APIs take precedence.
- Use the **exact** `<frontend_dir>` and `<backend_dir>` from Step 1 (user answer or detected). Do not inject env-based or auto-detect logic unless the user asks for it.

## Hash routing

- When the same Flask app serves the SPA (one `index.html` for all non-API paths), the frontend should use `createHashRouter`. If you find `createBrowserRouter`, switch to `createHashRouter` so the server does not need per-route config.
