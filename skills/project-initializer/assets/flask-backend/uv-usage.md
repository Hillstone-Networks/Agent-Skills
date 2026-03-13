# 使用 uv 管理本项目

本后端项目使用 [uv](https://docs.astral.sh/uv/) 进行依赖与虚拟环境管理。按以下步骤即可在本地运行与开发。

## 1. 安装 uv

**Linux / macOS（推荐）**：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows（PowerShell）**：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

或使用 pip：`pip install uv`。安装后确认：`uv --version`。

## 2. 进入项目并安装依赖

在项目根目录执行：

```bash
cd /path/to/your-project
uv sync
```

- `uv sync` 会创建虚拟环境（若不存在）并安装 `pyproject.toml` 中的依赖，同时生成/更新 `uv.lock`。
- 之后所有命令建议在「该虚拟环境下」执行，方式有两种：
  - 使用 `uv run <命令>`（推荐），或
  - 先激活环境：`source .venv/bin/activate`（Linux/macOS）或 `.venv\Scripts\activate`（Windows），再直接运行命令。

## 3. 常用命令

| 用途           | 命令 |
|----------------|------|
| 安装依赖并锁库 | `uv sync` |
| 运行 Flask 应用 | `uv run flask run` 或 `uv run python -m flask run` |
| 运行测试       | `uv run pytest` |
| 添加新依赖     | `uv add <包名>`，如 `uv add marshmallow` |
| 添加开发依赖   | `uv add --dev pytest pytest-cov` |
| 导出 requirements.txt（兼容 CI/镜像） | `uv export --no-hashes -o requirements.txt` |

若在 `pyproject.toml` 中配置了 `[project.scripts]` 或自定义脚本，可用：

```bash
uv run your-command
```

## 4. 环境变量

复制示例并填写本地配置：

```bash
cp .env.example .env
# 编辑 .env，填写 SECRET_KEY、DATABASE_URL 等
```

运行前确保 `.env` 已就绪（或通过系统环境变量注入）。

## 5. 快速启动

```bash
uv sync
cp .env.example .env   # 首次需配置 .env
uv run flask run
```

默认访问：http://127.0.0.1:5000（以实际配置为准）。

## 6. 使用 pip 的用户

若暂不使用 uv，可根据 `pyproject.toml` 自行创建虚拟环境并安装依赖；或先导出再安装：

```bash
uv export --no-hashes -o requirements.txt
pip install -r requirements.txt
```

建议在协作与 CI 中统一使用 uv，以保证环境与锁文件一致。
