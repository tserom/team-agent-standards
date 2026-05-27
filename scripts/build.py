#!/usr/bin/env python3
"""方案 B：各 Agent 产物在 generated/<agent-id>/ 下（可见目录名），构建时只清空该子目录。"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDELINES = ROOT / "guidelines"
CURSOR_MANIFEST = ROOT / "cursor-manifest.json"
AGENT_MANIFEST = ROOT / "agent-manifest.json"
GENERATED = ROOT / "generated"
TEMPLATES = ROOT / "templates"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def read_guideline(name: str) -> str:
    path = GUIDELINES / name
    if not path.is_file():
        raise FileNotFoundError(f"guideline not found: {path}")
    return path.read_text(encoding="utf-8").strip() + "\n"


def read_header(name: str) -> str:
    path = TEMPLATES / name
    if not path.is_file():
        raise FileNotFoundError(f"header template not found: {path}")
    return path.read_text(encoding="utf-8").rstrip() + "\n\n"


def yaml_quote(s: str) -> str:
    if any(c in s for c in ':"\'\n#'):
        escaped = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return s


def build_frontmatter(rule: dict) -> str:
    lines = ["---"]
    lines.append(f"description: {yaml_quote(rule['description'])}")
    if rule.get("alwaysApply"):
        lines.append("alwaysApply: true")
    else:
        lines.append("alwaysApply: false")
    globs = rule.get("globs")
    if globs:
        lines.append("globs:")
        for g in globs:
            lines.append(f"  - {g}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def guidelines_body(cursor_manifest: dict) -> str:
    parts: list[str] = []
    for rule in cursor_manifest["rules"]:
        parts.append(read_guideline(rule["guideline"]).rstrip())
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def agent_dir(agent: dict) -> Path:
    return GENERATED / agent["id"]


def prepare_agent_dir(agent: dict) -> Path:
    """只重建 generated/<agent-id>/，不触碰其它 Agent 目录。"""
    out = agent_dir(agent)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    return out


def build_cursor(agent: dict, cursor_manifest: dict) -> list[Path]:
    base = prepare_agent_dir(agent)
    rules_dir = base / agent["dir"]
    rules_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for rule in cursor_manifest["rules"]:
        body = read_guideline(rule["guideline"])
        content = build_frontmatter(rule) + body
        if not content.endswith("\n"):
            content += "\n"
        out = rules_dir / rule["output"]
        out.write_text(content, encoding="utf-8")
        written.append(out)
    return written


def build_markdown_agent(agent: dict, cursor_manifest: dict) -> Path:
    base = prepare_agent_dir(agent)
    header = read_header(agent["header"])
    body = guidelines_body(cursor_manifest)
    content = (header + body).rstrip() + "\n"
    out = base / agent["file"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out


def find_agent(manifest: dict, agent_id: str) -> dict:
    for agent in manifest["agents"]:
        if agent["id"] == agent_id:
            return agent
    known = ", ".join(a["id"] for a in manifest["agents"])
    raise SystemExit(f"Unknown agent: {agent_id!r}\nAvailable: {known}")


def build_output_label(agent: dict) -> str:
    if agent.get("type") == "cursor":
        return f"{agent['dir']}/*.mdc"
    return agent["file"]


def print_copy_hint(agent: dict, written: list[Path]) -> None:
    base = agent_dir(agent)
    rel_base = base.relative_to(ROOT)
    install = Path(agent["installTo"])
    project = "/path/to/your-project"

    print()
    print(f"Built {agent['name']} -> {rel_base}/")
    for path in written:
        print(f"  - {path.relative_to(ROOT)}")
    print()
    print("Copy to your project:")
    if agent.get("type") == "cursor":
        print(f"  mkdir -p {project}/{install.parent}")
        print(f"  cp -R {rel_base}/{agent['dir']} {project}/{install.parent}/")
    elif install.name == Path(agent["file"]).name and len(install.parts) == 1:
        print(f"  cp {rel_base}/{agent['file']} {project}/")
    else:
        print(f"  mkdir -p {project}/{install.parent}")
        print(f"  cp {rel_base}/{agent['file']} {project}/{install}")


def list_agents(manifest: dict) -> None:
    print("Available agents (each writes only to generated/<id>/):")
    for agent in manifest["agents"]:
        print(f"  {agent['id']:<12} {agent['name']}")
        print(f"               -> generated/{agent['id']}/{build_output_label(agent)}")
        print(f"               install -> {agent['installTo']}")
    print()
    print("Usage: python3 scripts/build.py <agent-id>")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build team standards for one agent (output under generated/<id>/).",
    )
    parser.add_argument(
        "agent",
        nargs="?",
        help="Agent id, e.g. cursor, claude (see --list)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available agent ids",
    )
    args = parser.parse_args(argv)

    agent_manifest = load_json(AGENT_MANIFEST)

    if args.list or not args.agent:
        list_agents(agent_manifest)
        return 0 if args.list else 1

    agent = find_agent(agent_manifest, args.agent)
    cursor_manifest = load_json(CURSOR_MANIFEST)
    GENERATED.mkdir(parents=True, exist_ok=True)

    if agent.get("type") == "cursor":
        written = build_cursor(agent, cursor_manifest)
    else:
        written = [build_markdown_agent(agent, cursor_manifest)]

    print_copy_hint(agent, written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
