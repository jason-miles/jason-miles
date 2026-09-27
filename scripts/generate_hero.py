#!/usr/bin/env python3
"""
Generate assets/hero.svg — the editorial profile banner.

Design: near-black (or warm-paper) canvas, embedded Space Grotesk, a single red
accent. Left column is an editorial masthead (kicker / name / tagline / fact
index); the right column is a custom "data-strata" signature mark — layered bars
that evoke a lakehouse, with a slow shimmer for restrained motion.

Local run:  GITHUB_TOKEN=... python3 scripts/generate_hero.py
"""
import json
import os
import urllib.request
from pathlib import Path

import brand

USER = "jason-miles"
OUT = Path(__file__).resolve().parent.parent / "assets" / "hero.svg"
W, H = 1200, 284
PAD = 64

# custom strata mark: per-row segment widths (px); layered "lakehouse" bars.
STRATA = [
    [40, 66],
    [96, 28, 44],
    [150],                 # accent
    [58, 104],
    [26, 38, 118],         # accent on last
    [176],
    [48, 88],
    [102, 56],             # accent on first
    [72],
]
ACCENTS = {(2, 0), (4, 2), (7, 0)}   # (row, segment) drawn in red
STRATA_X = 860
STRATA_TOP = 78
ROW_GAP = 21
SEG_H = 8
SEG_GAP = 8


def public_repo_count() -> int:
    req = urllib.request.Request(f"https://api.github.com/users/{USER}")
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    req.add_header("User-Agent", "jason-miles-profile-bot")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return int(json.load(r).get("public_repos", 0))
    except Exception:
        return 0


def strata() -> str:
    """The signature mark. Neutral bars (theme-adaptive) + 3 red accents, with a
    slow staggered opacity shimmer that reads as data settling into layers."""
    out = []
    for i, row in enumerate(STRATA):
        y = STRATA_TOP + i * ROW_GAP
        x = STRATA_X
        for j, w in enumerate(row):
            accent = (i, j) in ACCENTS
            fill = f'fill="{brand.RED}"' if accent else 'class="muted"'
            base = 0.9 if accent else 0.42
            hi = 1.0 if accent else 0.72
            begin = round(i * 0.28 + j * 0.16, 2)
            out.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="{SEG_H}" rx="4" {fill} opacity="{base}">'
                f'<animate attributeName="opacity" values="{base};{hi};{base}" '
                f'dur="4.2s" begin="{begin}s" repeatCount="indefinite" '
                f'calcMode="spline" keyTimes="0;0.5;1" keySplines="0.4 0 0.2 1;0.4 0 0.2 1"/>'
                f'</rect>')
            x += w + SEG_GAP
    return "".join(out)


def build() -> str:
    repos = public_repo_count()
    repo_txt = f"{repos} PUBLIC REPOS" if repos else "PUBLIC REPOS"
    kicker = "SENIOR SOLUTIONS ARCHITECT · DATABRICKS"
    tagline = "Turning data & AI ambition into production on the Lakehouse."
    index = f"8× DATABRICKS CERTIFIED   ·   {repo_txt}   ·   LONDON — EMEA — SA"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Jason Miles — Senior Solutions Architect at Databricks">
  <title>Jason Miles — Senior Solutions Architect · Databricks</title>
{brand.theme_style()}
  <!-- canvas -->
  <rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="{brand.RADIUS}" class="ink hair" stroke-width="1.5"/>

  <!-- signature accent tick -->
  <rect x="{PAD}" y="44" width="28" height="3" rx="1.5" fill="{brand.RED}">
    <animate attributeName="width" values="28;46;28" dur="5s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.4 0 0.2 1;0.4 0 0.2 1"/>
  </rect>

  <!-- masthead -->
  <text x="{PAD}" y="78" class="muted" font-size="13" font-weight="500" letter-spacing="3.6">{kicker}</text>
  <text x="{PAD}" y="152" class="txt" font-size="68" font-weight="700" letter-spacing="-1.6">Jason Miles</text>
  <text x="{PAD}" y="200" class="txt" font-size="18" font-weight="500">{brand.esc(tagline)}</text>

  <!-- fact index -->
  <circle cx="{PAD+4}" cy="248" r="4" fill="{brand.RED}">
    <animate attributeName="opacity" values="1;0.3;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <text x="{PAD+20}" y="253" class="muted" font-size="12.5" font-weight="500" letter-spacing="2.2">{index}</text>

  <!-- custom data-strata signature -->
  {strata()}
</svg>
"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
