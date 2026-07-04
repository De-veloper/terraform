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


def resource_rows(change):
    actions = tuple(change["actions"])
    before = change.get("before") or {}
    after = change.get("after") or {}
    after_unknown = change.get("after_unknown") or {}
    rows = []

    if actions == ("create",):
        for key in sorted(set(after) | set(after_unknown)):
            value = "(known after apply)" if after_unknown.get(key) else fmt(after.get(key))
            rows.append(f"| 🟢 Add | `{key}` | {value} |")
    elif actions == ("delete",):
        for key in sorted(before):
            rows.append(f"| 🔴 Remove | `{key}` | {fmt(before[key])} |")
    else:
        for key in sorted(set(before) | set(after) | set(after_unknown)):
            b, a, unknown = before.get(key), after.get(key), after_unknown.get(key)
            if unknown:
                rows.append(f"| 🟡 Change | `{key}` | (known after apply) |")
            elif b == a:
                continue
            elif key not in before or b is None:
                rows.append(f"| 🟢 Add | `{key}` | {fmt(a)} |")
            elif key not in after or a is None:
                rows.append(f"| 🔴 Remove | `{key}` | {fmt(b)} |")
            else:
                rows.append(f"| 🟡 Change | `{key}` | {fmt(b)} → {fmt(a)} |")

    return rows


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
        rows = resource_rows(rc["change"])

        lines.append(f"### {label} `{rc['address']}`")
        lines.append("")
        if rows:
            lines.append("| Status | Attribute | Value |")
            lines.append("|---|---|---|")
            lines.extend(rows)
        lines.append("")

    if not lines:
        lines = ["_No resource changes._"]

    print("\n".join(lines))


if __name__ == "__main__":
    main()
