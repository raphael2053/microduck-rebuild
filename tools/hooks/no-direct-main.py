#!/usr/bin/env python3
"""禁止直接提交或推送到 main（PreToolUse hook）。

所有改动必须走 PR。本 hook 拦两类：
  1. 在 main 分支上 git commit
  2. 向 main 推送（无论 `git push origin main` 还是在 main 上裸 `git push`）

放行 --dry-run、`git push` 到其它分支、以及非 git 命令。
"""
import json, re, subprocess, sys


def branch():
    try:
        r = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                           capture_output=True, text=True, timeout=5)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def main():
    try:
        p = json.load(sys.stdin)
    except Exception:
        return 0  # 解析不了就放行，hook 不该成为新的故障源

    if p.get("tool_name") != "Bash":
        return 0
    cmd = (p.get("tool_input", {}) or {}).get("command", "")
    if "git" not in cmd:
        return 0
    if "--dry-run" in cmd:
        return 0

    cur = branch()

    # 1) 在 main 上 commit
    if re.search(r'\bgit\s+(-\S+\s+)*commit\b', cmd) and cur == "main":
        sys.stderr.write(
            "已拦截：当前在 main 分支上 commit。\n\n"
            "本项目所有改动必须走 PR，禁止直接提交到 main。\n"
            "先开分支：  git checkout -b <type>/<描述>\n"
            "再提交、推分支、开 PR。\n")
        return 2

    # 2) 推送到 main
    push = re.search(r'\bgit\s+(-\S+\s+)*push\b([^&|;]*)', cmd)
    if push:
        args = push.group(2) or ""
        targets_main = re.search(r'(^|\s)(\S+:)?main(\s|$)', args) or \
                       re.search(r'\bHEAD:main\b', args)
        bare_push_on_main = (not args.strip() or
                             re.fullmatch(r'\s*(-\S+\s*)*\S+\s*', args)) and cur == "main"
        if targets_main or bare_push_on_main:
            sys.stderr.write(
                f"已拦截：向 main 推送（当前分支 {cur or '未知'}）。\n\n"
                "本项目所有改动必须走 PR，禁止直接推 main。\n"
                "推分支：  git push -u origin <分支名>\n"
                "再开 PR： gh pr create\n")
            return 2
    return 0


sys.exit(main())
