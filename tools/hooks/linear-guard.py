#!/usr/bin/env python3
"""Linear workspace 护栏（PreToolUse hook）。

两条规则，都来自 CLAUDE.md：
  1. 本项目绝不使用公司 workspace —— 拦截全部 mcp__linear-company__*
  2. 本项目的 issue 归 MDR team —— 拦截建到别的 team 的 save_issue / save_project

规则 1 是硬红线：写进公司 workspace 不可接受，且没有一次性的结构解法，
必须在每一次调用上成立。自然语言只是请求，这里要的是保证。
"""
import json, os, sys

TEAM = os.environ.get("MICRODUCK_LINEAR_TEAM", "microduck-rebuild")
TEAM_KEY = "MDR"

def main():
    try:
        p = json.load(sys.stdin)
    except Exception:
        return 0  # 解析不了就放行，hook 不该成为新的故障源

    tool = p.get("tool_name", "")
    if not tool.startswith("mcp__linear"):
        return 0

    if tool.startswith("mcp__linear-company__"):
        sys.stderr.write(
            f"已拦截 {tool}\n\n"
            "本项目禁止使用公司 Linear workspace（见 CLAUDE.md）。\n"
            "个人项目与公司项目不得混淆：不建 issue、不改 issue、不读公司数据。\n"
            f"改用 mcp__linear-personal__* 并指定 team「{TEAM}」（{TEAM_KEY}）。\n")
        return 2

    if tool in ("mcp__linear-personal__save_issue", "mcp__linear-personal__save_project"):
        ti = p.get("tool_input", {}) or {}
        teams = [ti["team"]] if ti.get("team") else []
        teams += ti.get("addTeams") or []
        teams += ti.get("setTeams") or []
        if ti.get("leadTeam"):
            teams.append(ti["leadTeam"])
        bad = [t for t in teams if isinstance(t, str)
               and t.strip().lower() not in (TEAM.lower(), TEAM_KEY.lower())]
        if bad:
            sys.stderr.write(
                f"已拦截 {tool}\n\n"
                f"team 写成了 {bad!r}，本项目的 Linear 条目必须归「{TEAM}」（{TEAM_KEY}）。\n"
                "Linear 的 issue 前缀取自 team key，建错 team 会拿到错误的编号前缀。\n")
            return 2
    return 0

sys.exit(main())
