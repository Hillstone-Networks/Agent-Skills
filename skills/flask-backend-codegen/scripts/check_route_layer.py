#!/usr/bin/env python3
"""
检查路由层是否违规：是否在 *_api.py 中直接使用 db.session / .query / Model 等。
Usage: python check_route_layer.py app/routes/user_api.py
"""
import re
import sys
from pathlib import Path

ROUTE_VIOLATIONS = [
    (r"db\.session\.", "路由层禁止直接使用 db.session"),
    (r"\.query\.", "路由层禁止直接使用 .query（应在 Service 中）"),
    (r"from app\.models\.", "路由层不应直接导入 Model（应通过 Service）"),
]


def check_file(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    for pattern, msg in ROUTE_VIOLATIONS:
        if re.search(pattern, text):
            errors.append(f"{path}: {msg}")
    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python check_route_layer.py <routes/*_api.py> [files...]", file=sys.stderr)
        return 2
    all_errors = []
    for p in sys.argv[1:]:
        path = Path(p)
        if not path.exists():
            all_errors.append(f"{p}: file not found")
            continue
        all_errors.extend(check_file(path))
    if all_errors:
        for e in all_errors:
            print(e, file=sys.stderr)
        return 1
    print("OK: no route-layer violations found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
