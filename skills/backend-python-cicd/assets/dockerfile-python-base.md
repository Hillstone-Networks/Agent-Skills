# Dockerfile Python 基础镜像与 pip 约定

本文件为 **私有镜像源参考** 的 Python 部分：生成或校验 Python 项目 Dockerfile 时**必须**遵守以下约定，尤其是基础镜像与 pip/uv 镜像源，不得使用公网默认源或不指定源。

## 0. 前置：检查项目依赖文件

**生成或校验 Dockerfile 之前，必须确认项目根目录已存在对应依赖文件**，否则 `uv sync` / `pip install` 会失败、构建报错：

| 依赖方式 | 必须存在的文件 | 说明 |
|----------|----------------|------|
| **uv**   | `pyproject.toml`、`uv.lock` | 缺一不可；无 `pyproject.toml` 或 `uv.lock` 时 `uv sync` 无法执行 |
| **pip**  | `requirements.txt`（或 Dockerfile 中声明的其它依赖文件） | 不存在则 `pip install -r requirements.txt` 失败 |

- 若使用 uv 但项目中没有 `pyproject.toml` 或 `uv.lock`，应**先**引导用户执行 `uv init`、补充依赖并执行 `uv lock`，再生成/使用该 Dockerfile。
- 文档与说明中应写明前置条件：「项目须已具备 pyproject.toml + uv.lock（或 requirements.txt）」。

## 1. 基础镜像：使用私有镜像源

**基础镜像默认使用私有镜像源**：

```dockerfile
# requirement 与 project 阶段均基于此镜像（或 requirement 为 FROM，project 为 FROM requirement 阶段）
FROM docker.dic.hillstonenet.com/library/python:3.12-slim
```

- 保证构建与运行环境一致，且不依赖公网拉取。
- 若项目需其他 Python 版本，可改为同源下的其他 tag（如 `3.11-slim`），仍建议使用 **docker.dic.hillstonenet.com/library/python:** 前缀。

## 2. pip 安装：必须使用清华 PyPI 源

**所有使用 pip 安装依赖的步骤，必须通过清华 PyPI 镜像源** `https://pypi.tuna.tsinghua.edu.cn/simple`，以加速国内构建并减少公网不稳定因素。


```dockerfile
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
```

### 约定要点

- **禁止**在 Dockerfile 中仅写 `pip install -r requirements.txt` 而不指定国内源。
- 使用 `--no-cache-dir` 可减小镜像层体积。
- `--trusted-host pypi.tuna.tsinghua.edu.cn` 在 HTTPS 校验场景下避免证书告警。
