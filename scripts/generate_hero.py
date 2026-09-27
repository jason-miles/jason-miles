#!/usr/bin/env python3
"""
Generate assets/hero.svg — the animated profile banner.

A single self-contained SVG that:
  * renders a Databricks-red -> amber gradient header with a dot-grid motif
  * types out a rotating set of taglines (per-character reveal + riding caret)
    using SMIL, which GitHub runs for SVG loaded via <img>
  * shows a live stat line (public repo count is pulled at generation time)
  * adapts to GitHub light/dark via prefers-color-scheme

Run nightly by .github/workflows/profile-refresh.yml, or locally:
    GITHUB_TOKEN=... python3 scripts/generate_hero.py
"""
import json
import os
import urllib.request
from pathlib import Path

import brand

USER = "jason-miles"
OUT = Path(__file__).resolve().parent.parent / "assets" / "hero.svg"

W, H = 1200, 268
PAD = 56

PHRASES = [
    "Turning data & AI ambition into production.",
    "Lakehouse architecture · governance · GenAI.",
    "From POC to production on Databricks.",
    "Agents, RAG & Model Serving, at scale.",
]

# typed-line geometry
TYPE_FS = 27            # font size of the rotating line
CHAR_W = TYPE_FS * 0.60  # mono char-width estimate for caret placement
TYPE_X = PAD + 26        # x where phrase text starts (after the "› " prompt)
TYPE_Y = 178


def public_repo_count() -> int:
    """Live count of the user's public repos; falls back gracefully offline."""
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


def typed_line() -> str:
    """
    Build the rotating typed line. Each phrase gets a clipPath whose width ramps
    0 -> full within its slice of one shared loop (dur = T), plus a caret that
    rides the clip edge and blinks. Opacity windows hand off between phrases.
    """
    n = len(PHRASES)
    slot = 3.4                     # seconds a phrase is on screen
    T = round(n * slot, 2)         # total loop length
    typ = 1.5 / T                  # fraction of the loop spent typing a phrase
    f = 1.0 / n                    # fraction of the loop per phrase

    clips, texts, carets = [], [], []
    for i, phrase in enumerate(PHRASES):
        start = i * f
        end = (i + 1) * f
        type_end = start + typ
        end_x = TYPE_X + len(phrase) * CHAR_W

        # clipPath rect: width 0 until this phrase's window, ramps to full, holds
        clips.append(
            f'<clipPath id="clip{i}"><rect x="{TYPE_X}" y="{TYPE_Y-30}" '
            f'width="0" height="42">'
            f'<animate attributeName="width" '
            f'values="0;0;{end_x-TYPE_X:.0f};{end_x-TYPE_X:.0f}" '
            f'keyTimes="0;{start:.4f};{type_end:.4f};1" '
            f'dur="{T}s" repeatCount="indefinite" calcMode="linear"/>'
            f'</rect></clipPath>'
        )

        # phrase text, revealed through its clip, faded in/out over its window
        eps = 0.004
        op_kt = f"0;{max(start-eps,0):.4f};{start:.4f};{end-eps:.4f};{end:.4f};1"
        op_v = "0;0;1;1;0;0" if i < n - 1 else "1;1;1;1;0;0"
        if i == 0:
            op_kt = f"0;{start:.4f};{end-eps:.4f};{end:.4f};1"
            op_v = "1;1;1;0;0"
        texts.append(
            f'<g clip-path="url(#clip{i})">'
            f'<text x="{TYPE_X}" y="{TYPE_Y}" class="type" '
            f'font-family="{brand.MONO}" font-size="{TYPE_FS}">{_esc(phrase)}'
            f'</text></g>'
            f'<animate xlink:href="#g{i}" attributeName="opacity" '
            f'values="{op_v}" keyTimes="{op_kt}" dur="{T}s" '
            f'repeatCount="indefinite"/>'
        )
        # wrap text group with an id so opacity animation can target it
        texts[-1] = f'<g id="g{i}">' + texts[-1].split("<animate")[0] + "</g>" + \
            "<animate" + texts[-1].split("<animate", 1)[1]

        # riding caret: x tracks the clip edge, opacity blinks
        carets.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
            f'keyTimes="0;{max(start-eps,0):.4f};{start:.4f};{end-eps:.4f};{end:.4f};1" '
            f'dur="{T}s" repeatCount="indefinite"/>'
            f'<rect y="{TYPE_Y-24}" width="3" height="30" fill="{brand.RED}">'
            f'<animate attributeName="x" '
            f'values="{TYPE_X};{TYPE_X};{end_x:.0f};{end_x:.0f}" '
            f'keyTimes="0;{start:.4f};{type_end:.4f};1" dur="{T}s" '
            f'repeatCount="indefinite" calcMode="linear"/>'
            f'<animate attributeName="opacity" values="1;1;0;0;1" '
            f'keyTimes="0;0.45;0.5;0.95;1" dur="1s" repeatCount="indefinite"/>'
            f'</rect></g>'
        )

    prompt = (f'<text x="{PAD}" y="{TYPE_Y}" font-family="{brand.MONO}" '
              f'font-size="{TYPE_FS}" fill="{brand.RED}" '
              f'font-weight="700">&#8250;</text>')
    return "<defs>" + "".join(clips) + "</defs>" + prompt + \
        "".join(texts) + "".join(carets)


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build() -> str:
    repos = public_repo_count()
    repo_txt = f"{repos} public repositories" if repos else "public repositories"
    stat = (f"{repo_txt}  ·  8 Databricks certifications  ·  "
            f"London → UK · EMEA · South Africa")

    style = brand.theme_style(f"""
    .name  {{ font-weight: 800; letter-spacing: -0.5px; }}
    .type  {{ fill: {brand.TEXT_DARK}; }}
    @media (prefers-color-scheme: light) {{ .type {{ fill: {brand.TEXT_LIGHT}; }} }}
  """)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Jason Miles — Senior Solutions Architect at Databricks">
  <title>Jason Miles — Senior Solutions Architect · Databricks</title>
{style}
  <defs>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{brand.RED}"/>
      <stop offset="55%" stop-color="{brand.ORANGE}"/>
      <stop offset="100%" stop-color="{brand.AMBER}"/>
    </linearGradient>
    <radialGradient id="glow" cx="15%" cy="0%" r="75%">
      <stop offset="0%" stop-color="{brand.RED}" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="{brand.RED}" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- canvas -->
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{brand.RADIUS}" class="bg line" stroke-width="1.5"/>
  {brand.dot_grid(W, H)}
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{brand.RADIUS}" fill="url(#glow)"/>
  <!-- accent rail -->
  <rect x="1" y="1" width="7" height="{H-2}" rx="3.5" fill="url(#accent)"/>
  <!-- animated accent sweep along the top -->
  <rect x="{PAD}" y="46" width="120" height="4" rx="2" fill="url(#accent)">
    <animate attributeName="width" values="0;340;0" dur="6s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.4 0 0.2 1;0.4 0 0.2 1"/>
  </rect>

  <!-- identity -->
  <text x="{PAD}" y="112" class="txt name" font-family="{brand.SANS}" font-size="60">Jason Miles</text>
  <text x="{PAD}" y="146" class="muted" font-family="{brand.SANS}" font-size="21" letter-spacing="0.3px">Senior Solutions Architect · Databricks</text>

  <!-- rotating typed line -->
  {typed_line()}

  <!-- live stat line -->
  <circle cx="{PAD+4}" cy="226" r="4.5" fill="{brand.RED}">
    <animate attributeName="opacity" values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/>
  </circle>
  <text x="{PAD+20}" y="231" class="muted" font-family="{brand.SANS}" font-size="16">{_esc(stat)}</text>
</svg>
"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
