#!/usr/bin/env python3
"""
Generate assets/now.svg — the live "Currently building" strip.

Pulls the most recently *pushed* public repos at generation time and renders
them as three cards (name · description · "updated N ago"), with a pulsing live
dot. Regenerated nightly by the workflow so the profile always reads as active.

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
W = 1200
HEAD = 52
CARD_H = 120
GAP = 20
# repos we never want to surface as "building" (infra / meta)
SKIP = {"jason-miles", "github-stats"}


def recent_repos(n=3):
    url = (f"https://api.github.com/users/{USER}/repos"
           f"?sort=pushed&per_page=30&type=owner")
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
    out = []
    for repo in data:
        if repo["name"] in SKIP or repo.get("fork") or repo.get("archived"):
            continue
        out.append(repo)
        if len(out) == n:
            break
    return out


def ago(iso: str) -> str:
    try:
        t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except Exception:
        return ""
    d = datetime.now(timezone.utc) - t
    days = d.days
    if days <= 0:
        return "today"
    if days == 1:
        return "yesterday"
    if days < 30:
        return f"{days}d ago"
    if days < 365:
        return f"{days // 30}mo ago"
    return f"{days // 365}y ago"


def _esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _wrap(text: str, width: int, size: int = 13):
    """Naive word-wrap to <=2 lines for the card description."""
    if not text:
        return ["Recent work in this repository."]
    cpl = max(8, int(width / (size * 0.52)))
    words, lines, cur = text.split(), [], ""
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
    if len(lines) == 2 and len(" ".join(words)) > sum(len(x) for x in lines):
        lines[1] = lines[1][:cpl - 1].rstrip() + "…"
    return lines[:2]


def card(repo, x):
    cw = (W - 2 * GAP - 2 * GAP) / 3
    y = HEAD
    name = _esc(repo["name"])
    desc = repo.get("description") or ""
    if not desc:
        lang = repo.get("language")
        desc = f"{lang} · active development" if lang else "Active development."
    desc_lines = _wrap(desc, cw - 44)
    rel = ago(repo.get("pushed_at", ""))
    s = [f'<rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="{CARD_H}" rx="12" class="panel"/>']
    s.append(f'<rect x="{x:.0f}" y="{y}" width="4" height="{CARD_H}" rx="2" fill="url(#nowaccent)"/>')
    s.append(f'<text x="{x+22:.0f}" y="{y+34}" class="txt" font-family="{brand.SANS}" '
             f'font-size="18" font-weight="700">{name}</text>')
    for i, ln in enumerate(desc_lines):
        s.append(f'<text x="{x+22:.0f}" y="{y+58+i*19}" class="muted" '
                 f'font-family="{brand.SANS}" font-size="13">{_esc(ln)}</text>')
    s.append(f'<circle cx="{x+27:.0f}" cy="{y+CARD_H-22}" r="3.5" fill="{brand.RED}"/>')
    s.append(f'<text x="{x+38:.0f}" y="{y+CARD_H-17}" class="muted" '
             f'font-family="{brand.MONO}" font-size="12">updated {rel}</text>')
    return "".join(s)


def build() -> str:
    repos = recent_repos(3)
    cw = (W - 2 * GAP - 2 * GAP) / 3
    if repos:
        cards = "".join(card(r, GAP + i * (cw + GAP)) for i, r in enumerate(repos))
    else:
        cards = (f'<text x="{W/2}" y="{HEAD+70}" text-anchor="middle" class="muted" '
                 f'font-family="{brand.SANS}" font-size="15">Recent public activity loads here.</text>')
    H = HEAD + CARD_H + 20
    today = datetime.now(timezone.utc).strftime("%d %b %Y")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Currently building — recent public repositories">
  <title>Currently building</title>
{brand.theme_style()}
  <defs>
    <linearGradient id="nowaccent" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{brand.RED}"/>
      <stop offset="100%" stop-color="{brand.AMBER}"/>
    </linearGradient>
  </defs>
  <circle cx="{GAP+6}" cy="26" r="6" fill="{brand.RED}">
    <animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite"/>
  </circle>
  <text x="{GAP+22}" y="31" class="txt" font-family="{brand.SANS}" font-size="17" font-weight="700">Currently building</text>
  <text x="{W-GAP}" y="31" text-anchor="end" class="muted" font-family="{brand.MONO}" font-size="12">auto-updated nightly · {today}</text>
  {cards}
</svg>
"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
