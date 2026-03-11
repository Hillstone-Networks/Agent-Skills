#!/usr/bin/env python3
"""
Validate agent role definition JSON files against the expected structure.
Usage: python validate_roles.py [path/to/role1.json] [path/to/role2.json] ...
"""
import json
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL = {"id", "displayName", "scenario", "scope"}
REQUIRED_SECTIONS = {
    "inputExpectation": {"upstreamRoles", "artifacts", "requiredFormat"},
    "outputSpec": {"artifacts", "qualityCriteria"},
    "handoff": {"targetRoles", "format", "checklist"},
}


def validate_role(data: dict, path: str) -> list[str]:
    errors = []
    if not isinstance(data, dict):
        return [f"{path}: root must be a JSON object"]

    missing = REQUIRED_TOP_LEVEL - set(data.keys())
    if missing:
        errors.append(f"{path}: missing required fields: {missing}")

    for section, keys in REQUIRED_SECTIONS.items():
        if section not in data:
            errors.append(f"{path}: missing section '{section}'")
            continue
        val = data[section]
        if not isinstance(val, dict):
            errors.append(f"{path}: '{section}' must be an object")
            continue
        missing_in = keys - set(val.keys())
        if missing_in:
            errors.append(f"{path}: in '{section}' missing: {missing_in}")

    if "constraints" in data and not isinstance(data["constraints"], list):
        errors.append(f"{path}: 'constraints' must be an array")

    if "id" in data and not isinstance(data["id"], str):
        errors.append(f"{path}: 'id' must be a string (kebab-case)")

    return errors


def main() -> int:
    paths = sys.argv[1:] if len(sys.argv) > 1 else []
    if not paths:
        print("Usage: python validate_roles.py <role1.json> [role2.json ...]", file=sys.stderr)
        return 2

    all_errors = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            all_errors.append(f"{p}: file not found")
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            all_errors.append(f"{p}: invalid JSON - {e}")
            continue
        all_errors.extend(validate_role(data, str(path)))

    if all_errors:
        for e in all_errors:
            print(e, file=sys.stderr)
        return 1
    print("OK: all role definitions valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
