#!/usr/bin/env python3
import json
import sys

ICONS = {
    ("create",): "🟢 Create",
    ("update",): "🟡 Update",
    ("delete",): "🔴 Destroy",
    ("delete", "create"): "🔁 Replace",
    ("create", "delete"): "🔁 Replace",
    ("read",): "🔍 Read",
}


def fmt(value):
    if value is None:
        return "null"
    text = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
    return text if len(text) <= 60 else text[:57] + "..."


def main():
    plan_path = sys.argv[1] if len(sys.argv) > 1 else "plan.json"
    with open(plan_path) as f:
        plan = json.load(f)

    lines = []
    for rc in plan.get("resource_changes", []):
        actions = tuple(rc["change"]["actions"])
        if actions == ("no-op",):
            continue

        label = ICONS.get(actions, "⚪ " + ",".join(actions))
        lines.append(f"### {label} `{rc['address']}`")
        lines.append("")

        before = rc["change"].get("before") or {}
        after = rc["change"].get("after") or {}
        after_unknown = rc["change"].get("after_unknown") or {}

        concrete_rows = []
        unknown_keys = []
        for key in sorted(set(before) | set(after) | set(after_unknown)):
            b, a, unknown = before.get(key), after.get(key), after_unknown.get(key)
            if unknown:
                unknown_keys.append(key)
            elif b == a:
                continue
            elif key not in before or b is None:
                concrete_rows.append(f"| 🟢 Add | `{key}` | {fmt(a)} |")
            elif key not in after or a is None:
                concrete_rows.append(f"| 🔴 Remove | `{key}` | {fmt(b)} |")
            else:
                concrete_rows.append(f"| 🟡 Change | `{key}` | {fmt(b)} → {fmt(a)} |")

        if concrete_rows:
            lines.append("| Status | Attribute | Value |")
            lines.append("|---|---|---|")
            lines.extend(concrete_rows)
            lines.append("")

        if unknown_keys:
            keys_str = ", ".join(f"`{k}`" for k in unknown_keys)
            lines.append(f"❔ **Known after apply ({len(unknown_keys)}):** {keys_str}")
            lines.append("")

    if not lines:
        lines = ["_No resource changes._"]

    print("\n".join(lines))


if __name__ == "__main__":
    main()
