#!/usr/bin/env python3
"""
Generate assets/proj-*.svg — one editorial "spec card" per featured project.

No browser chrome, no gradients. Each card is a numbered spec sheet: an index
numeral, a category label, a hairline rule, a monochrome line-art schematic
whose shape matches the real product (dashboard / exam / medallion pipeline /
workshop) with a single red accent, and the project name set in Space Grotesk.

Local run:  python3 scripts/generate_projects.py
"""
from pathlib import Path
import brand

ASSETS = Path(__file__).resolve().parent.parent / "assets"
W, H = 640, 400
PAD = 28
HEADER_Y = 68        # hairline under the header
FOOTER_Y = 344       # hairline above the footer

PROJECTS = [
    dict(slug="sentinel", idx="01", title="Sentinel", tag="FRAUD & AML · DATABRICKS APP",
         layout="dashboard",
         kpis=[("ALERTS", "1.2k"), ("RESOLVED", "947"), ("MODELS", "6")]),
    dict(slug="vitality", idx="02", title="Vitality Pulse", tag="SHARED-VALUE ANALYTICS · GENIE",
         layout="dashboard",
         kpis=[("MEMBERS", "2.4M"), ("REWARDS", "£18M"), ("CLAIMS", "−9%")]),
    dict(slug="mlpro", idx="03", title="ML Pro · Exam Prep", tag="FASTAPI + REACT",
         layout="exam", q="Q42 · ADVANCED MLOPS"),
    dict(slug="depro", idx="04", title="DE Pro · Exam Prep", tag="FASTAPI + REACT",
         layout="exam", q="Q28 · STRUCTURED STREAMING"),
    dict(slug="sap", idx="05", title="AI · SAP × Databricks", tag="REFERENCE ARCHITECTURE",
         layout="pipeline"),
    dict(slug="vibe", idx="06", title="Vibe Coding Workshop", tag="WORKSHOP · NOV 2025",
         layout="workshop"),
]


def _header(idx, tag):
    return (
        f'<text x="{PAD}" y="52" class="txt" font-size="34" font-weight="700" opacity="0.16">{idx}</text>'
        f'<text x="{W-PAD}" y="40" text-anchor="end" class="muted" font-size="11.5" '
        f'font-weight="500" letter-spacing="2">{brand.esc(tag)}</text>'
        f'<line x1="{PAD}" y1="{HEADER_Y}" x2="{W-PAD}" y2="{HEADER_Y}" class="hair" stroke-width="1"/>'
    )


def _footer(title):
    return (
        f'<line x1="{PAD}" y1="{FOOTER_Y}" x2="{W-PAD}" y2="{FOOTER_Y}" class="hair" stroke-width="1"/>'
        f'<rect x="{PAD}" y="{FOOTER_Y+18}" width="10" height="10" rx="2" fill="{brand.RED}"/>'
        f'<text x="{PAD+22}" y="{FOOTER_Y+28}" class="txt" font-size="19" font-weight="700">{brand.esc(title)}</text>'
    )


def _panel(x, y, w, h, r=10):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="panel panelstroke" stroke-width="1"/>'


def _dashboard(kpis):
    """3 KPI tiles + a bar chart (tallest bar red) + a red trend line."""
    y0 = 92
    s = []
    tw = (W - 2 * PAD - 2 * 16) / 3
    for i, (lab, val) in enumerate(kpis):
        x = PAD + i * (tw + 16)
        s.append(_panel(x, y0, tw, 74))
        dot = brand.RED if i == 0 else None
        s.append(f'<circle cx="{x+18:.0f}" cy="{y0+22}" r="3.5" '
                 f'{"fill=\""+brand.RED+"\"" if dot else "class=\"muted\""}/>')
        s.append(f'<text x="{x+30:.0f}" y="{y0+26}" class="muted" font-size="10.5" letter-spacing="1.2">{lab}</text>')
        s.append(f'<text x="{x+18:.0f}" y="{y0+58}" class="txt" font-size="26" font-weight="700">{val}</text>')
    # bar chart panel
    by = y0 + 90
    bpw = (W - 2 * PAD) * 0.6
    s.append(_panel(PAD, by, bpw, 150))
    heights = [38, 66, 50, 82, 60, 96, 72]
    bw = 18
    step = (bpw - 44) / len(heights)
    tallest = heights.index(max(heights))
    for i, hgt in enumerate(heights):
        x = PAD + 26 + i * step
        fill = f'fill="{brand.RED}"' if i == tallest else 'class="muted"'
        s.append(f'<rect x="{x:.0f}" y="{by+124-hgt}" width="{bw}" height="{hgt}" rx="3" {fill} '
                 f'{"" if i==tallest else "opacity=\"0.55\""}/>')
    # trend panel with red line (the accent)
    tx = PAD + bpw + 16
    tpw = W - PAD - tx
    s.append(_panel(tx, by, tpw, 150))
    x0 = tx + 20
    xs = [x0 + k * (tpw - 40) / 5 for k in range(6)]
    ys = [by + 108, by + 86, by + 96, by + 60, by + 72, by + 34]
    pts = " ".join(f"{px:.0f},{py:.0f}" for px, py in zip(xs, ys))
    s.append(f'<polyline points="{pts}" fill="none" stroke="{brand.RED}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
    for px, py in zip(xs, ys):
        s.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="3" fill="{brand.RED}"/>')
    return "".join(s)


def _exam(q):
    """Progress bar (red = active) + question + four options, one selected."""
    y0 = 92
    s = [_panel(PAD, y0, W - 2 * PAD, 220)]
    ix = PAD + 24
    iw = W - 2 * PAD - 48
    s.append(f'<rect x="{ix}" y="{y0+26}" width="{iw}" height="6" rx="3" class="muted" opacity="0.25"/>')
    s.append(f'<rect x="{ix}" y="{y0+26}" width="{iw*0.42:.0f}" height="6" rx="3" fill="{brand.RED}"/>')
    s.append(f'<text x="{ix}" y="{y0+64}" class="txt" font-size="14" font-weight="700" letter-spacing="0.5">{brand.esc(q)}</text>')
    for i in range(2):
        s.append(f'<rect x="{ix}" y="{y0+80+i*15}" width="{iw-i*80}" height="7" rx="3.5" class="muted" opacity="0.28"/>')
    for i in range(4):
        yy = y0 + 122 + i * 24
        sel = i == 2
        s.append(f'<rect x="{ix}" y="{yy}" width="{iw}" height="18" rx="6" '
                 f'{"fill=\""+brand.RED+"\" fill-opacity=\"0.10\" stroke=\""+brand.RED+"\"" if sel else "class=\"panelstroke\" fill=\"none\""} stroke-width="1"/>')
        s.append(f'<circle cx="{ix+14}" cy="{yy+9}" r="5" fill="none" stroke="{brand.RED if sel else brand.MUTED_D}" stroke-width="1.6"/>')
        if sel:
            s.append(f'<circle cx="{ix+14}" cy="{yy+9}" r="2.4" fill="{brand.RED}"/>')
        s.append(f'<rect x="{ix+30}" y="{yy+5}" width="{150+i*26}" height="7" rx="3.5" class="muted" opacity="0.42"/>')
    return "".join(s)


def _pipeline():
    """Medallion flow with red directional arrows (the accent)."""
    cy = 168
    stages = ["SAP", "BRONZE", "SILVER", "GOLD"]
    s = []
    bw, gap = 116, 28
    x = PAD + 6
    for i, lab in enumerate(stages):
        s.append(_panel(x, cy - 34, bw, 68))
        s.append(f'<text x="{x+bw/2:.0f}" y="{cy-4}" text-anchor="middle" class="txt" font-size="13" font-weight="700" letter-spacing="1">{lab}</text>')
        s.append(f'<rect x="{x+24:.0f}" y="{cy+12}" width="{bw-48}" height="6" rx="3" class="muted" opacity="0.3"/>')
        if i < len(stages) - 1:
            ax = x + bw + 5
            s.append(f'<line x1="{ax}" y1="{cy}" x2="{ax+gap-10}" y2="{cy}" stroke="{brand.RED}" stroke-width="2"/>')
            s.append(f'<path d="M{ax+gap-10} {cy} l-6 -4 v8 z" fill="{brand.RED}"/>')
        x += bw + gap
    # governance strip
    gy = cy + 66
    s.append(_panel(PAD + 6, gy, W - 2 * PAD - 12, 50))
    s.append(f'<circle cx="{PAD+34}" cy="{gy+25}" r="4" fill="{brand.RED}"/>')
    s.append(f'<text x="{PAD+50}" y="{gy+21}" class="txt" font-size="13" font-weight="700">Unity Catalog governance</text>')
    s.append(f'<text x="{PAD+50}" y="{gy+39}" class="muted" font-size="11">lineage · access · AI/BI &amp; Model Serving</text>')
    return "".join(s)


def _workshop():
    """A slide panel with a red Build pill + a terminal panel, single accent."""
    y0 = 92
    sw = 300
    s = [_panel(PAD, y0, sw, 220)]
    s.append(f'<rect x="{PAD+24}" y="{y0+26}" width="150" height="10" rx="5" fill="{brand.RED}"/>')
    for i in range(4):
        s.append(f'<rect x="{PAD+24}" y="{y0+54+i*20}" width="{240-i*34}" height="7" rx="3.5" class="muted" opacity="0.32"/>')
    s.append(f'<rect x="{PAD+24}" y="{y0+152}" width="112" height="32" rx="7" fill="{brand.RED}"/>')
    s.append(f'<text x="{PAD+80}" y="{y0+173}" text-anchor="middle" fill="#ffffff" font-size="13" font-weight="700">Build →</text>')
    # terminal
    tx = PAD + sw + 16
    tw = W - PAD - tx
    s.append(f'<rect x="{tx}" y="{y0}" width="{tw}" height="220" rx="10" fill="{brand.INK}" stroke="{brand.HAIR_D}" stroke-width="1"/>')
    lines = [("$ databricks bundle deploy", brand.RED),
             ("  agent deployed", brand.MUTED_D),
             ("$ ask genie \"top risks?\"", brand.RED),
             ("  analysing gold tables", brand.MUTED_D),
             ("  3 insights ready", brand.MUTED_D)]
    for i, (t, c) in enumerate(lines):
        s.append(f'<text x="{tx+18}" y="{y0+40+i*30}" fill="{c}" font-size="12" font-weight="500">{brand.esc(t)}</text>')
    return "".join(s)


def build(p):
    if p["layout"] == "dashboard":
        body = _dashboard(p["kpis"])
    elif p["layout"] == "exam":
        body = _exam(p["q"])
    elif p["layout"] == "pipeline":
        body = _pipeline()
    else:
        body = _workshop()
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{brand.esc(p['title'])} — {brand.esc(p['tag'])}">
  <title>{brand.esc(p['title'])}</title>
{brand.theme_style()}
  <rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="{brand.RADIUS}" class="ink hair" stroke-width="1.5"/>
  {_header(p['idx'], p['tag'])}
  {body}
  {_footer(p['title'])}
</svg>
"""


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        (ASSETS / f"proj-{p['slug']}.svg").write_text(build(p), encoding="utf-8")
        print(f"wrote proj-{p['slug']}.svg")
