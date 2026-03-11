# Dockerfile Python 基础镜像约定

生成或校验 Python 项目 Dockerfile 时，**基础镜像默认使用私有镜像源**：

```dockerfile
# requirement 与 project 阶段均基于此镜像（或 requirement 为 FROM，project 为 FROM requirement 阶段）
FROM docker.dic.hillstonenet.com/library/python:3.12-slim
```

- 保证构建与运行环境一致，且不依赖公网拉取。
- 若项目需其他 Python 版本，可改为同源下的其他 tag（如 `3.11-slim`），仍建议使用 **docker.dic.hillstonenet.com/library/python:** 前缀。
