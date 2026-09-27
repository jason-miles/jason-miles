"""
Brand kit — the single source of visual truth for Jason Miles' GitHub profile.

Every generated SVG (hero banner, "now" strip, project preview cards) imports
these tokens so the whole profile — plus the github.io homepage — reads as one
designed system rather than a pile of independent widgets.

Design language
---------------
* Base:      GitHub-native surfaces (#0d1117 dark / #ffffff light) so assets sit
             flush against the README canvas with no seams.
* Accent:    Databricks red -> warm orange sweep (#FF3621 -> #FF5F46 -> #FFA600).
* Type:      A single humanist sans stack for headings/body, a mono stack for
             the "terminal" typing line. System fonts only — SVG-as-<img> on
             GitHub can't reliably load web fonts, so we never depend on them.
* Motif:     A faint dot-grid + a single glowing accent sweep. Used sparingly.
* Geometry:  14px card radius, 1px hairline borders, generous padding.
"""

# --- palette -----------------------------------------------------------------
RED        = "#FF3621"   # Databricks primary
ORANGE     = "#FF5F46"
AMBER       = "#FFA600"
INK_DARK   = "#0d1117"   # GitHub dark canvas
INK_LIGHT  = "#ffffff"   # GitHub light canvas
PANEL_DARK  = "#161b22"  # raised surface (dark)
PANEL_LIGHT = "#f6f8fa"  # raised surface (light)
LINE_DARK  = "#30363d"   # hairline border (dark)
LINE_LIGHT = "#d0d7de"   # hairline border (light)
TEXT_DARK  = "#e6edf3"   # primary text on dark
TEXT_LIGHT = "#1f2328"   # primary text on light
MUTED_DARK  = "#8b949e"  # secondary text on dark
MUTED_LIGHT = "#59636e"  # secondary text on light

# --- type --------------------------------------------------------------------
SANS = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,"
        "sans-serif,'Apple Color Emoji','Segoe UI Emoji'")
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

# --- geometry ----------------------------------------------------------------
RADIUS = 14

# --- shields.io stack chips (shared by the project gallery) ------------------
def chip(label: str, color: str, logo: str = "", logo_color: str = "white") -> str:
    """Return a shields.io badge URL fragment used as a stack chip."""
    import urllib.parse
    text = urllib.parse.quote(label)
    url = f"https://img.shields.io/badge/{text}-{color}?style=flat-square"
    if logo:
        url += f"&logo={logo}&logoColor={logo_color}"
    return url


def theme_style(extra: str = "") -> str:
    """
    A reusable <style> block that makes a single SVG adapt to GitHub's light and
    dark themes via prefers-color-scheme (which GitHub honours for SVG-as-image).
    Elements opt in with class names: .bg .panel .line .txt .muted .hl
    """
    return f"""
  <style>
    .bg    {{ fill: {INK_LIGHT}; }}
    .panel {{ fill: {PANEL_LIGHT}; }}
    .line  {{ stroke: {LINE_LIGHT}; }}
    .txt   {{ fill: {TEXT_LIGHT}; }}
    .muted {{ fill: {MUTED_LIGHT}; }}
    .dot   {{ fill: {LINE_LIGHT}; }}
    @media (prefers-color-scheme: dark) {{
      .bg    {{ fill: {INK_DARK}; }}
      .panel {{ fill: {PANEL_DARK}; }}
      .line  {{ stroke: {LINE_DARK}; }}
      .txt   {{ fill: {TEXT_DARK}; }}
      .muted {{ fill: {MUTED_DARK}; }}
      .dot   {{ fill: {LINE_DARK}; }}
    }}
    {extra}
  </style>"""


def dot_grid(width: int, height: int, gap: int = 26, r: float = 1.1,
             x0: int = 0, y0: int = 0) -> str:
    """A faint dot-grid motif used as a subtle background texture."""
    dots = []
    y = y0 + gap
    while y < height:
        x = x0 + gap
        while x < width:
            dots.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="dot" opacity="0.5"/>')
            x += gap
        y += gap
    return "".join(dots)
