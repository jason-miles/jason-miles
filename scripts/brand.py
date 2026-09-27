"""
Brand kit — the single source of visual truth for Jason Miles' GitHub profile.

Design language: "engineered editorial"
--------------------------------------
Deliberately restrained, so it reads as a bespoke design system rather than a
templated README. The rules:

* One typeface, embedded.  Space Grotesk (subset, weights 500/700) is embedded
  as a data-URI @font-face so every asset renders in the same real type on any
  machine — no system-font fallback, which is the tell of a generated profile.
* One accent.  Databricks red (#FF3621) is used sparingly — a single element
  per composition — against a near-black / warm-paper neutral base. No
  multi-stop gradients, no glows, no dot-grids.
* Hairlines & space.  1px rules, generous negative space, real alignment.
* Adapts to GitHub light & dark via prefers-color-scheme.
"""
from _fontdata import FONT_FACE

# --- palette -----------------------------------------------------------------
RED        = "#FF3621"   # Databricks red — the only accent
RED_SOFT   = "#FF5F46"
INK        = "#0A0C10"   # near-black canvas (dark)
PAPER      = "#FBFBF9"   # warm off-white canvas (light)
# dark theme
TEXT_D  = "#EDF0F3"
MUTED_D = "#767E88"
HAIR_D  = "#20252C"
PANEL_D = "#12161C"
# light theme
TEXT_L  = "#0A0C10"
MUTED_L = "#6E7681"
HAIR_L  = "#E4E5E1"
PANEL_L = "#F1F1ED"

# --- type --------------------------------------------------------------------
SG = "'SG',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

RADIUS = 12


def theme_style(extra: str = "") -> str:
    """Embedded font + theme-adaptive class palette.

    Classes: .ink (canvas fill) .txt .muted .hair (stroke) .panel (fill)
             .panelfill (as fill via class) — plus .red constants used inline.
    """
    return f"""
  <style>
    {FONT_FACE}
    text {{ font-family: {SG}; }}
    .ink   {{ fill: {PAPER}; }}
    .txt   {{ fill: {TEXT_L}; }}
    .muted {{ fill: {MUTED_L}; }}
    .hair  {{ stroke: {HAIR_L}; }}
    .panel {{ fill: {PANEL_L}; }}
    .panelstroke {{ stroke: {HAIR_L}; }}
    @media (prefers-color-scheme: dark) {{
      .ink   {{ fill: {INK}; }}
      .txt   {{ fill: {TEXT_D}; }}
      .muted {{ fill: {MUTED_D}; }}
      .hair  {{ stroke: {HAIR_D}; }}
      .panel {{ fill: {PANEL_D}; }}
      .panelstroke {{ stroke: {HAIR_D}; }}
    }}
    {extra}
  </style>"""


def esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
