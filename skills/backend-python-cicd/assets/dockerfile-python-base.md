# Dockerfile Python 基础镜像与 pip 约定

生成或校验 Python 项目 Dockerfile 时，需遵守以下约定。

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
