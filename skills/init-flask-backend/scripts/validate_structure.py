#!/usr/bin/env python3
"""
校验 Flask API 项目目录与必要文件是否符合规范。
Usage: python validate_structure.py /path/to/project
"""
import sys
from pathlib import Path

REQUIRED = [
    "app/__init__.py",
    "app/config.py",
    "app/extensions.py",
    "app/routes/__init__.py",
    "app/routes/main_api.py",
    "app/models/__init__.py",
    "app/service/__init__.py",
    "app/schemas/__init__.py",
    "app/utils/api_util.py",
    "tests/conftest.py",
]
OPTIONAL = [
    "app/permission/constants.py",
    "app/utils/logger_util.py",
    "app/utils/jwt_util.py",
    ".env.example",
    "pyproject.toml",
    "README.md",
    "Dockerfile",
]


def validate(root: Path) -> list[str]:
    errors = []
    root = root.resolve()
    if not root.is_dir():
        return [f"Not a directory: {root}"]

    for rel in REQUIRED:
        p = root / rel
        if not p.exists():
            errors.append(f"Missing required: {rel}")
        elif rel.endswith(".py") and p.suffix == ".py" and not p.is_file():
            errors.append(f"Expected file: {rel}")

    for rel in OPTIONAL:
        p = root / rel
        if not p.exists():
            pass  # optional, only report in verbose mode if needed

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python validate_structure.py /path/to/project", file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    errors = validate(root)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("OK: project structure valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
