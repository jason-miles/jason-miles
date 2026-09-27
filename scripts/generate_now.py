#!/usr/bin/env python3
"""
Generate assets/now.svg — the editorial "Currently building" strip.

Matches the profile's engineered-editorial language: a tracked kicker, a hairline
rule, and three columns (index / repo / description / relative time) divided by
hairlines. Pulls the most recently pushed public repos at generation time; one
red accent (the live dot). Regenerated nightly by the workflow.

Local run:  GITHUB_TOKEN=... python3 scripts/generate_now.py
"""
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import brand

USER = "jason-miles"
OUT = Path(__file__).resolve().parent.parent / "assets" / "now.svg"
W, H = 1200, 210
PAD = 40
HEAD_Y = 40
COL_TOP = 88
SKIP = {"jason-miles", "github-stats"}

# Curated flagship repos to feature, in order. Their "updated N ago" is still
# pulled live — this pins *which* repos show, not fake timestamps. If a curated
# repo is missing, we top up with the most recently pushed non-curated repo.
CURATED = [
    "sentinel-app",
    "discovery-vitality-pulse-app-V1",
    "momentum-life-claims-processing-app",
]


def recent_repos(n=3):
    url = f"https://api.github.com/users/{USER}/repos?sort=pushed&per_page=100&type=owner"
    req = urllib.request.Request(url)
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    req.add_header("User-Agent", "jason-miles-profile-bot")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.load(r)
    except Exception:
        return []
    by_name = {repo["name"]: repo for repo in data}
    out = [by_name[name] for name in CURATED if name in by_name]
    # top up with most-recently-pushed repos if any curated ones are missing
    for repo in data:
        if len(out) >= n:
            break
        if (repo["name"] in SKIP or repo["name"] in CURATED
                or repo.get("fork") or repo.get("archived")):
            continue
        out.append(repo)
    return out[:n]


def ago(iso):
    try:
        t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except Exception:
        return ""
    days = (datetime.now(timezone.utc) - t).days
    if days <= 0:
        return "TODAY"
    if days == 1:
        return "YESTERDAY"
    if days < 30:
        return f"{days} DAYS AGO"
    if days < 365:
        m = days // 30
        return f"{m} MONTH AGO" if m == 1 else f"{m} MONTHS AGO"
    y = days // 365
    return f"{y} YEAR AGO" if y == 1 else f"{y} YEARS AGO"


def _wrap(text, cpl):
    words, lines, cur = (text or "").split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= cpl:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
        if len(lines) == 2:
            break
    if cur and len(lines) < 2:
        lines.append(cur)
    if len(lines) == 2 and len(cur) > cpl:
        lines[1] = lines[1][:cpl - 1].rstrip() + "…"
    return lines[:2] or [""]


def column(repo, i, x, cw):
    name = brand.esc(repo["name"])
    desc = repo.get("description") or ""
    if not desc:
        lang = repo.get("language")
        desc = f"{lang} · active development" if lang else "Active development"
    cpl = max(10, int(cw / 7.4))
    lines = _wrap(desc, cpl)
    s = [f'<text x="{x:.0f}" y="{COL_TOP}" class="muted" font-size="12" font-weight="700" opacity="0.4">0{i+1}</text>']
    s.append(f'<text x="{x:.0f}" y="{COL_TOP+30}" class="txt" font-size="19" font-weight="700">{name}</text>')
    for k, ln in enumerate(lines):
        s.append(f'<text x="{x:.0f}" y="{COL_TOP+56+k*19}" class="muted" font-size="13" font-weight="500">{brand.esc(ln)}</text>')
    s.append(f'<circle cx="{x+4:.0f}" cy="{COL_TOP+96}" r="3" fill="{brand.RED}"/>')
    s.append(f'<text x="{x+16:.0f}" y="{COL_TOP+100}" class="muted" font-size="11" font-weight="500" letter-spacing="1.5">{ago(repo.get("pushed_at",""))}</text>')
    return "".join(s)


def build():
    repos = recent_repos(3)
    today = datetime.now(timezone.utc).strftime("%d %b %Y").upper()
    inner = W - 2 * PAD
    cols = 3
    gap = 40
    cw = (inner - (cols - 1) * gap) / cols
    body, dividers = [], []
    for i in range(cols):
        x = PAD + i * (cw + gap)
        if i < len(repos):
            body.append(column(repos[i], i, x, cw))
        if i > 0:
            dx = x - gap / 2
            dividers.append(f'<line x1="{dx:.0f}" y1="{COL_TOP-18}" x2="{dx:.0f}" y2="{H-30}" class="hair" stroke-width="1"/>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Currently building — recent public repositories">
  <title>Currently building</title>
{brand.theme_style()}
  <rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="{brand.RADIUS}" class="ink hair" stroke-width="1.5"/>
  <circle cx="{PAD+5}" cy="{HEAD_Y-4}" r="5" fill="{brand.RED}">
    <animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="{PAD+20}" y="{HEAD_Y}" class="txt" font-size="14" font-weight="700" letter-spacing="2.4">CURRENTLY BUILDING</text>
  <text x="{W-PAD}" y="{HEAD_Y}" text-anchor="end" class="muted" font-size="11" font-weight="500" letter-spacing="1.8">AUTO-UPDATED · {today}</text>
  <line x1="{PAD}" y1="{HEAD_Y+18}" x2="{W-PAD}" y2="{HEAD_Y+18}" class="hair" stroke-width="1"/>
  {''.join(dividers)}
  {''.join(body)}
</svg>
"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
