#!/usr/bin/env python3
"""
Generate assets/proj-*.svg — one branded "app-window" preview card per featured
project. Each card is a stylised product screenshot: window chrome + a schematic
UI whose *shape* matches what the project actually is (dashboard / exam / medallion
pipeline / workshop). This gives the Featured Projects gallery real visual weight
without needing live screenshots, and every card shares the brand kit so the row
reads as one designed system.

Local run:  python3 scripts/generate_projects.py
"""
from pathlib import Path
import brand

ASSETS = Path(__file__).resolve().parent.parent / "assets"
W, H = 640, 360
BAR = 44            # window title-bar height

PROJECTS = [
    dict(slug="sentinel", title="Sentinel — Fraud & AML",
         tag="DATABRICKS APP", host="sentinel.databricksapps.com",
         layout="dashboard",
         kpis=[("ALERTS", brand.RED, "1.2k"), ("RESOLVED", brand.AMBER, "947"),
               ("MODELS", "#28c840", "6")]),
    dict(slug="vitality", title="Discovery Vitality Pulse",
         tag="DATABRICKS APP · GENIE", host="vitality-pulse.databricksapps.com",
         layout="dashboard",
         kpis=[("MEMBERS", brand.RED, "2.4M"), ("REWARDS", brand.AMBER, "£18M"),
               ("CLAIMS", "#28c840", "−9%")]),
    dict(slug="mlpro", title="DBX ML Professional — Exam Prep",
         tag="FASTAPI + REACT", host="dbx-mlpro-cert.app",
         layout="exam", q="Q42 · Advanced MLOps"),
    dict(slug="depro", title="DBX Data Engineer Pro — Exam Prep",
         tag="FASTAPI + REACT", host="dbx-depro-cert.app",
         layout="exam", q="Q28 · Structured Streaming"),
    dict(slug="sap", title="Operationalizing AI · SAP × Databricks",
         tag="REFERENCE ARCHITECTURE", host="github.com/jason-miles",
         layout="pipeline"),
    dict(slug="vibe", title="Vibe Coding Workshop",
         tag="WORKSHOP · NOV 2025", host="github.com/jason-miles",
         layout="workshop"),
]


def _chrome(title_pill: str) -> str:
    dots = "".join(
        f'<circle cx="{22+i*20}" cy="{BAR/2}" r="6" fill="{c}"/>'
        for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")))
    return (
        f'<rect x="1" y="1" width="{W-2}" height="{BAR}" rx="{brand.RADIUS}" class="panel"/>'
        f'<rect x="1" y="{BAR-brand.RADIUS}" width="{W-2}" height="{brand.RADIUS}" class="panel"/>'
        f'{dots}'
        f'<rect x="92" y="11" width="{W-184}" height="22" rx="11" class="bg line" stroke-width="1"/>'
        f'<text x="{W/2}" y="26" text-anchor="middle" class="muted" '
        f'font-family="{brand.MONO}" font-size="12">{title_pill}</text>'
    )


def _dashboard(kpis=None) -> str:
    """Sidebar + 3 KPI tiles + a bar chart + a trend line — a fraud/analytics app."""
    kpis = kpis or [("ALERTS", brand.RED, "1.2k"), ("RESOLVED", brand.AMBER, "947"),
                    ("MODELS", "#28c840", "6")]
    y0 = BAR + 20
    s = []
    # sidebar
    s.append(f'<rect x="20" y="{y0}" width="120" height="{H-y0-24}" rx="10" class="panel"/>')
    for i in range(5):
        w = 78 if i else 96
        col = brand.RED if i == 0 else None
        s.append(f'<rect x="34" y="{y0+22+i*30}" width="{w}" height="10" rx="5" '
                 f'{"fill=\""+brand.RED+"\"" if col else "class=\"line\" stroke=\"none\" fill-opacity=\"0.35\" fill=\"gray\""}/>')
    # KPI tiles
    tx = 160
    for i, (lab, c, val) in enumerate(kpis):
        x = tx + i*150
        s.append(f'<rect x="{x}" y="{y0}" width="132" height="70" rx="10" class="panel"/>')
        s.append(f'<rect x="{x+14}" y="{y0+16}" width="8" height="8" rx="4" fill="{c}"/>')
        s.append(f'<text x="{x+30}" y="{y0+24}" class="muted" font-family="{brand.SANS}" font-size="10">{lab}</text>')
        s.append(f'<text x="{x+14}" y="{y0+54}" class="txt" font-family="{brand.SANS}" font-size="26" font-weight="700">{val}</text>')
    # bar chart
    by = y0 + 96
    s.append(f'<rect x="{tx}" y="{by}" width="282" height="150" rx="10" class="panel"/>')
    heights = [40, 78, 55, 96, 68, 110, 84]
    for i, h in enumerate(heights):
        x = tx + 22 + i*36
        s.append(f'<rect x="{x}" y="{by+130-h}" width="20" height="{h}" rx="4" fill="url(#paccent)"/>')
    # trend line panel
    ly = by
    s.append(f'<rect x="{tx+298}" y="{ly}" width="150" height="150" rx="10" class="panel"/>')
    pts = "466,236 494,214 522,224 550,190 578,200 606,168"
    s.append(f'<polyline points="{pts}" fill="none" stroke="{brand.RED}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    for p in pts.split():
        x, y = p.split(",")
        s.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{brand.RED}"/>')
    return "".join(s)


def _exam(q="Q42 · Advanced MLOps") -> str:
    """A question card, progress bar, answer options — an exam-prep app."""
    y0 = BAR + 22
    s = [f'<rect x="24" y="{y0}" width="{W-48}" height="{H-y0-24}" rx="12" class="panel"/>']
    s.append(f'<rect x="48" y="{y0+22}" width="180" height="8" rx="4" fill="{brand.RED}"/>')
    s.append(f'<rect x="48" y="{y0+22}" width="{W-96}" height="8" rx="4" class="line" fill="none" stroke-width="1"/>')
    s.append(f'<text x="48" y="{y0+66}" class="txt" font-family="{brand.SANS}" font-size="15" font-weight="700">{_esc(q)}</text>')
    for i in range(2):
        s.append(f'<rect x="48" y="{y0+82+i*16}" width="{W-140-i*90}" height="8" rx="4" class="muted" fill="gray" fill-opacity="0.35"/>')
    opts = ["A", "B", "C", "D"]
    for i, o in enumerate(opts):
        yy = y0 + 128 + i*40
        hot = i == 2
        s.append(f'<rect x="48" y="{yy}" width="{W-96}" height="30" rx="8" '
                 f'{"fill=\""+brand.RED+"\" fill-opacity=\"0.14\" stroke=\""+brand.RED+"\"" if hot else "class=\"bg line\""} stroke-width="1.5"/>')
        s.append(f'<circle cx="70" cy="{yy+15}" r="8" fill="none" stroke="{brand.RED if hot else brand.MUTED_DARK}" stroke-width="2"/>')
        if hot:
            s.append(f'<circle cx="70" cy="{yy+15}" r="4" fill="{brand.RED}"/>')
        s.append(f'<rect x="90" y="{yy+11}" width="{200+i*30}" height="8" rx="4" class="muted" fill="gray" fill-opacity="0.4"/>')
    return "".join(s)


def _pipeline() -> str:
    """Source -> Bronze -> Silver -> Gold medallion flow — a reference architecture."""
    y0 = BAR + 60
    stages = [("SAP", "#9aa0a6"), ("BRONZE", "#cd7f32"), ("SILVER", "#aab2bd"), ("GOLD", brand.AMBER)]
    s = []
    bw, gap = 118, 26
    x = 34
    cy = y0 + 40
    for i, (lab, c) in enumerate(stages):
        s.append(f'<rect x="{x}" y="{cy-38}" width="{bw}" height="76" rx="12" class="panel"/>')
        s.append(f'<rect x="{x}" y="{cy-38}" width="6" height="76" rx="3" fill="{c}"/>')
        s.append(f'<text x="{x+bw/2+3}" y="{cy-6}" text-anchor="middle" class="txt" font-family="{brand.SANS}" font-size="13" font-weight="700">{lab}</text>')
        s.append(f'<rect x="{x+22}" y="{cy+10}" width="{bw-44}" height="7" rx="3.5" class="muted" fill="gray" fill-opacity="0.4"/>')
        if i < len(stages)-1:
            ax = x + bw + 4
            s.append(f'<path d="M{ax} {cy} h{gap-8}" stroke="{brand.RED}" stroke-width="2.5"/>')
            s.append(f'<path d="M{ax+gap-8} {cy} l-6 -4 v8 z" fill="{brand.RED}"/>')
        x += bw + gap
    # a governance/AI banner below
    s.append(f'<rect x="34" y="{cy+70}" width="{W-68}" height="52" rx="12" class="panel"/>')
    s.append(f'<circle cx="62" cy="{cy+96}" r="10" fill="url(#paccent)"/>')
    s.append(f'<text x="82" y="{cy+92}" class="txt" font-family="{brand.SANS}" font-size="13" font-weight="700">Unity Catalog governance</text>')
    s.append(f'<text x="82" y="{cy+110}" class="muted" font-family="{brand.SANS}" font-size="11">lineage · access · AI/BI &amp; Model Serving</text>')
    return "".join(s)


def _workshop() -> str:
    """A slide + a terminal block — a hands-on workshop."""
    y0 = BAR + 22
    s = [f'<rect x="24" y="{y0}" width="330" height="{H-y0-24}" rx="12" class="panel"/>']
    s.append(f'<rect x="46" y="{y0+22}" width="180" height="12" rx="6" fill="{brand.RED}"/>')
    for i in range(4):
        s.append(f'<rect x="46" y="{y0+52+i*22}" width="{280-i*30}" height="8" rx="4" class="muted" fill="gray" fill-opacity="0.4"/>')
    s.append(f'<rect x="46" y="{y0+150}" width="120" height="34" rx="8" fill="url(#paccent)"/>')
    s.append(f'<text x="106" y="{y0+172}" text-anchor="middle" fill="white" font-family="{brand.SANS}" font-size="13" font-weight="700">Build →</text>')
    # terminal
    tx = 372
    s.append(f'<rect x="{tx}" y="{y0}" width="{W-tx-24}" height="{H-y0-24}" rx="12" fill="#0b1020"/>')
    lines = [("$ databricks bundle deploy", brand.AMBER),
             ("✓ agent deployed", "#28c840"),
             ("$ ask genie \"top risks?\"", brand.AMBER),
             ("→ analysing gold tables…", "#8b949e"),
             ("✓ 3 insights ready", "#28c840")]
    for i, (t, c) in enumerate(lines):
        s.append(f'<text x="{tx+16}" y="{y0+34+i*26}" fill="{c}" font-family="{brand.MONO}" font-size="12">{t}</text>')
    return "".join(s)


LAYOUTS = dict(dashboard=_dashboard, exam=_exam, pipeline=_pipeline, workshop=_workshop)


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(p: dict) -> str:
    if p["layout"] == "dashboard":
        body = _dashboard(p.get("kpis"))
    elif p["layout"] == "exam":
        body = _exam(p.get("q", "Q42 · Advanced MLOps"))
    else:
        body = LAYOUTS[p["layout"]]()
    title = _esc(p["title"])
    host = _esc(p["host"])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title}">
  <title>{title}</title>
{brand.theme_style()}
  <defs>
    <linearGradient id="paccent" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{brand.RED}"/>
      <stop offset="100%" stop-color="{brand.AMBER}"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{brand.RADIUS}" class="bg line" stroke-width="1.5"/>
  {_chrome(host)}
  {body}
  <!-- footer tag + title -->
  <rect x="0" y="{H-2}" width="{W}" height="2" fill="url(#paccent)"/>
  <text x="24" y="{BAR-58 if False else BAR+0}" opacity="0"></text>
</svg>
"""


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        out = ASSETS / f"proj-{p['slug']}.svg"
        out.write_text(build(p), encoding="utf-8")
        print(f"wrote {out.name}")
