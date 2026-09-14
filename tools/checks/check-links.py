#!/usr/bin/env python3
"""校验仓库内所有 markdown 的相对链接与锚点。

这个仓库当前几乎全部由交叉引用的文档构成，链接断裂是 harness 里少数
能被程序裁决的事情之一，所以做成脚本而不是写成约定。

用法：python3 tools/checks/check-links.py
退出码：0 全部解析成功，1 存在断链。
"""
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKIP_DIRS = {".git", ".omc", "node_modules", "target"}
LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
HEADING_RE = re.compile(r'^#{1,6}\s+(.+)$', re.M)


def slug(heading):
    """GitHub 风格锚点：转小写、去标点、空格转连字符。保留 CJK。"""
    s = re.sub(r'[^\w一-鿿\s-]', '', heading.strip().lower())
    return re.sub(r'\s+', '-', s).strip('-')


def collect_markdown(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        out.extend(os.path.join(dirpath, f) for f in filenames if f.endswith(".md"))
    return sorted(out)


def main():
    files = collect_markdown(REPO_ROOT)
    anchors = {
        f: {slug(h) for h in HEADING_RE.findall(open(f, encoding="utf-8").read())}
        for f in files
    }

    failures = []
    checked = 0
    for path in files:
        rel_src = os.path.relpath(path, REPO_ROOT)
        for lineno, line in enumerate(open(path, encoding="utf-8"), 1):
            for target in LINK_RE.findall(line):
                if target.startswith(("http://", "https://", "mailto:", "<")):
                    continue
                checked += 1
                file_part, _, anchor = target.partition("#")
                resolved = (
                    os.path.normpath(os.path.join(os.path.dirname(path), file_part))
                    if file_part else path
                )
                if file_part and not os.path.exists(resolved):
                    failures.append(f"{rel_src}:{lineno}  路径不存在  -> {target}")
                elif anchor and slug(anchor) not in anchors.get(resolved, set()):
                    failures.append(f"{rel_src}:{lineno}  锚点不存在  -> {target}")

    print(f"检查 {len(files)} 个 markdown 文件，{checked} 条内部链接")
    if failures:
        print(f"\n{len(failures)} 条断链：")
        for f in failures:
            print(f"  {f}")
        return 1
    print("全部解析成功")
    return 0


if __name__ == "__main__":
    sys.exit(main())
