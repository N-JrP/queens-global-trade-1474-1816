import streamlit as st
import time
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from pathlib import Path
import io
import base64
from typing import Optional




# =========================================================
# 0) PAGE CONFIG (must be the first Streamlit command)
# =========================================================
st.set_page_config(page_title="Queens Trade Explorer (1474–1816)", layout="wide")



# =========================================================
# 1) MAP BACKGROUND (Ancient world map as app watermark)
#    Put image here: assets/ancient_world_map.jpg (or .png)
# =========================================================
def image_file_to_data_uri(img_path: str) -> Optional[str]:
    p = Path(img_path)
    if not p.exists():
        return None
    ext = p.suffix.lower().replace(".", "")
    mime = "image/png" if ext == "png" else "image/jpeg"
    b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


MAP_URI = (
    image_file_to_data_uri("assets/ancient_world_map.jpg")
    or image_file_to_data_uri("assets/ancient_world_map.png")
)

if not MAP_URI:
    st.warning(
        "Map image not found. Place it at:\n"
        "assets/ancient_world_map.jpg (or .png)\n\n"
        "Example:\n"
        r"C:\Users\nehap\queens-global-trade-1474–1816\assets\ancient_world_map.jpg"
    )

# =========================================================
# 2) THEME: Medieval Manuscript / Parchment UI (with map)
# =========================================================
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&display=swap');

/* ---- Global Background ---- */
.stApp {{
    background: linear-gradient(180deg, #f6f0dc 0%, #f3e8c8 100%);
    font-family: "Playfair Display", Georgia, serif;
}}

/* Map layer (BEHIND UI) */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;

    background-image: url("{MAP_URI if MAP_URI else ""}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;

    opacity: 0.38;
    filter: sepia(0.55) contrast(1.05) saturate(0.85);
}}

/* Parchment veil (still BEHIND UI) */
.stApp::after {{
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 1;

    background: linear-gradient(
        180deg,
        rgba(246,240,220,0.68),
        rgba(243,232,200,0.88)
    );
}}

/* Ensure app content is ABOVE background layers */
[data-testid="stAppViewContainer"] {{
    position: relative;
    z-index: 5;
}}

/* ✅ Hide Streamlit Cloud header (fix overlap) */
header[data-testid="stHeader"] {{
  display: none !important;
}}

/* ✅ One scrollbar only */
html, body {{
  overflow-y: auto !important;
  height: auto !important;
}}

/* ---- Antique border frame ---- */
.block-container {{
    padding-top: 1.2rem;
    border: 1px solid rgba(120, 90, 40, 0.25);
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 8px 20px rgba(120, 90, 40, 0.12);
    margin-top: 10px;
    margin-left: 4px;
}}

/* ---- Typography ---- */
h1, h2, h3, h4 {{
    font-family: "Playfair Display", Georgia, serif;
    color: #5b4523;
}}
p, li, div, span, label {{
    color: #3e321f;
    font-family: "Playfair Display", Georgia, serif;
}}

/* ---- KPI metric boxes ---- */
div[data-testid="stMetric"] {{
    background: linear-gradient(145deg, #f4ecd8, #efe4c8);
    border: 1px solid #d8c9a6;
    border-radius: 14px;
    padding: 12px 14px;
    box-shadow: 0 4px 10px rgba(120, 90, 40, 0.12);
}}
div[data-testid="stMetricLabel"] {{
    color: #6a532f !important;
    font-weight: 600;
}}
div[data-testid="stMetricValue"] {{
    color: #4a381d !important;
}}

/* ---- Expander styling ---- */
div[data-testid="stExpander"] {{
    border: 1px solid rgba(120, 90, 40, 0.25);
    border-radius: 12px;
    background: rgba(244, 236, 216, 0.35);
}}

/* ---- Parchment HTML table ---- */
.parchment-table-wrap {{
    background: rgba(244, 236, 216, 0.65);
    border: 1px solid rgba(120, 90, 40, 0.22);
    border-radius: 14px;
    padding: 10px 12px;
    box-shadow: 0 4px 10px rgba(120, 90, 40, 0.08);
}}
.parchment-table-scroll {{
    overflow-y: auto;
    border-radius: 10px;
}}
.parchment-table {{
    width: 100%;
    border-collapse: collapse;
    font-family: Georgia, serif;
    font-size: 14px;
}}
.parchment-table thead th {{
    position: sticky;
    top: 0;
    background: #e9dcc0;
    color: #4a381d;
    border: 1px solid #d8c9a6;
    padding: 8px;
    text-align: left;
    z-index: 1;
}}
.parchment-table tbody td {{
    background: #f4ecd8;
    color: #3e321f;
    border: 1px solid #d8c9a6;
    padding: 8px;
    vertical-align: top;
}}
.parchment-table tbody tr:nth-child(even) td {{
    background: #f2e4c6;
}}
.parchment-table tbody tr:hover td {{
    background: #ead7b1;
    transition: background 0.12s ease-in-out;
}}

/* ---- About cards ---- */
.parchment-card {{
    background: linear-gradient(145deg, #f4ecd8, #efe4c8);
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #d8c9a6;
    box-shadow: 0 4px 10px rgba(120, 90, 40, 0.15);
}}
.parchment-card h4 {{
    margin-top: 0;
    color: #5a4a2f;
}}
.parchment-card ul {{
    padding-left: 18px;
}}

/* ---- Sidebar medieval styling ---- */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #f3e8c8 0%, #efe1bd 100%);
    border-right: 1px solid rgba(120, 90, 40, 0.25);
    box-shadow: 6px 0 18px rgba(120, 90, 40, 0.15);
    padding: 0.8rem 1rem !important;
}}
section[data-testid="stSidebar"]::after {{
    content: "";
    position: absolute;
    top: 0;
    right: -2px;
    width: 2px;
    height: 100%;
    background: linear-gradient(
        to bottom,
        transparent,
        #b59b5a,
        #d6b86a,
        #b59b5a,
        transparent
    );
    opacity: 0.85;
}}
section[data-testid="stSidebar"] * {{
    font-family: "Playfair Display", Georgia, serif;
    color: #4a381d !important;
}}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {{
    background-color: rgba(244,236,216,0.92) !important;
    color: #4a381d !important;
    border: 1px solid #d8c9a6 !important;
    border-radius: 12px !important;
}}

/* Apply same Royal Inquiry style to Selectboxes */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background-color: rgba(244,236,216,0.92) !important;
    color: #4a381d !important;
    border: 1px solid #d8c9a6 !important;
    border-radius: 12px !important;
}}

section[data-testid="stSidebar"] button {{
    background: linear-gradient(145deg, #efe4c8, #e6d7b2);
    border: 1px solid #c9b78d;
    color: #4a381d !important;
    border-radius: 10px;
}}
section[data-testid="stSidebar"] button:hover {{
    background: #e6d7b2;
}}

/* ✅ Center ONLY the "Clear the Council" button */
section[data-testid="stSidebar"] div.stButton > button {{
    display: block;
    margin: 0 auto;
    width: 100%;
    max-width: 260px;
}}

/* ✅ Sidebar widgets full width */
section[data-testid="stSidebar"] .stTextInput,
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stTextArea,
section[data-testid="stSidebar"] .stButton {{
  width: 100%;
}}

/* ✅ Radio in a card */
section[data-testid="stSidebar"] div[data-testid="stRadio"]{{
  background: rgba(244,236,216,0.40);
  border: 1px solid rgba(120,90,40,0.18);
  border-radius: 12px;
  padding: 10px 12px 8px 12px;
}}

/* ---- Manuscript Section Header ---- */
.manuscript-header {{
    display:flex;
    align-items:center;
    gap:12px;
    margin: 20px 0 12px 0;
}}
.manuscript-header .glyph {{
    font-size: 18px;
    opacity: 0.95;
    color: #6b4f2a;
    filter: drop-shadow(0 1px 0 rgba(255,255,255,0.35));
}}
.manuscript-header .label {{
    position: relative;
    padding: 9px 16px;
    border-radius: 12px;
    border: 1px solid rgba(120,90,40,0.35);
    background: linear-gradient(145deg, rgba(244,236,216,0.75), rgba(239,228,200,0.55));
    box-shadow: 0 5px 12px rgba(120,90,40,0.14);
    font-weight: 800;
    letter-spacing: 0.6px;
    color: #4a381d;
    white-space: nowrap;
    text-transform: uppercase;
}}
.manuscript-header .label:before,
.manuscript-header .label:after {{
    content:"";
    position:absolute;
    top: 50%;
    width: 10px;
    height: 10px;
    transform: translateY(-50%) rotate(45deg);
    background: rgba(244,236,216,0.70);
    border: 1px solid rgba(120,90,40,0.25);
}}
.manuscript-header .label:before {{ left: -6px; }}
.manuscript-header .label:after {{ right: -6px; }}

.manuscript-header .rule {{
    height: 2px;
    flex: 1;
    background: linear-gradient(to right,
        rgba(181,155,90,0.0),
        rgba(181,155,90,0.95),
        rgba(214,184,106,0.95),
        rgba(181,155,90,0.95),
        rgba(181,155,90,0.0)
    );
    opacity: 0.95;
    border-radius: 2px;
}}

/* ---- Portrait frames ---- */
.portrait-frame {{
  border-radius: 14px;
  padding: 16px;
  display: inline-block;
  box-shadow: 0 10px 22px rgba(0,0,0,0.18);
}}
.portrait-img {{
  display: block;
  max-width: 320px;
  width: 100%;
  height: auto;
  border-radius: 10px;
}}
.frame-renaissance {{
  background: linear-gradient(145deg, #d6b35a, #b08a3a);
  box-shadow:
    0 0 0 6px rgba(92,68,24,0.65),
    0 0 0 10px rgba(214,179,90,0.75),
    0 12px 26px rgba(0,0,0,0.25);
}}
.frame-baroque {{
  background: linear-gradient(145deg, #e1c06a, #b8872f);
  box-shadow:
    0 0 0 6px rgba(110,78,18,0.70),
    0 0 0 10px rgba(225,192,106,0.75),
    0 12px 26px rgba(0,0,0,0.26);
}}
.frame-wood {{
  background: linear-gradient(145deg, #5b3a22, #3b2414);
  box-shadow:
    0 0 0 6px rgba(28,18,10,0.75),
    0 0 0 10px rgba(110,78,52,0.55),
    0 12px 26px rgba(0,0,0,0.35);
}}
.portrait-name {{
  margin-top: 12px;
  text-align: center;
  font-weight: 700;
  font-size: 18px;
  color: #4b3b2b;
}}
.portrait-sub {{
  margin-top: 2px;
  text-align: center;
  font-size: 13px;
  font-style: italic;
  color: rgba(75,59,43,0.75);
}}

/* If any container is accidentally dimmed on Cloud, undo it */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
section.main {{
  opacity: 1 !important;
  filter: none !important;
}}

/* =========================================================
   ✅ LAYOUT FIX (ONLY THIS PART affects sidebar expand/collapse)
   - Sidebar stays fixed
   - Main content shifts with sidebar open/close
   - No overlap, no empty gap
   ========================================================= */

:root {{
  --qt-sidebar-expanded: 21rem;
  --qt-sidebar-collapsed: 3.5rem;
}}

/* Sidebar fixed */
section[data-testid="stSidebar"] {{
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  height: 100vh !important;
  overflow-y: auto !important;
  z-index: 9999 !important;

  width: var(--qt-sidebar-expanded) !important;
  min-width: var(--qt-sidebar-expanded) !important;
  max-width: var(--qt-sidebar-expanded) !important;
}}

/* Collapsed sidebar width */
section[data-testid="stSidebar"][aria-expanded="false"] {{
  width: var(--qt-sidebar-collapsed) !important;
  min-width: var(--qt-sidebar-collapsed) !important;
  max-width: var(--qt-sidebar-collapsed) !important;
}}

/* ✅ Make ONLY the right/main side scroll (sidebar stays fixed) */
[data-testid="stMain"] {{
  margin-left: var(--qt-sidebar-expanded) !important;
  transition: margin-left 0.2s ease;

  height: 100vh !important;
  overflow-y: auto !important;
}}

/* Hide the extra scrollbar on the page itself (so only main scrolls) */
html, body {{
  height: 100vh !important;
  overflow: hidden !important;
}}

/* Streamlit wrapper: don’t create another scroll container */
[data-testid="stAppViewContainer"] {{
  height: 100vh !important;
  overflow: hidden !important;
}}

/* Main shifts back when sidebar collapsed */
section[data-testid="stSidebar"][aria-expanded="false"] ~ [data-testid="stMain"] {{
  margin-left: var(--qt-sidebar-collapsed) !important;
}}

/* ✅ GOLD ORNAMENT LINE BETWEEN ✧ ✧ (sidebar dividers only) */
section[data-testid="stSidebar"] .council-divider .line{{
  height: 2px !important;
  flex: 1 !important;
  background: linear-gradient(
    to right,
    rgba(181,155,90,0.0),
    rgba(181,155,90,0.95),
    rgba(214,184,106,0.95),
    rgba(181,155,90,0.95),
    rgba(181,155,90,0.0)
  ) !important;
  opacity: 0.95 !important;
  border-radius: 2px !important;
}}

section[data-testid="stSidebar"] .council-divider .sigil{{
  color: #6b4f2a !important;
  opacity: 0.85 !important;
}}

</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# 3) HELPERS (tables, headers, chart styling)
# =========================================================
def manuscript_header(title: str, icon: str = "✦"):
    st.markdown(
        f"""
        <div class="manuscript-header">
          <div class="glyph">{icon}</div>
          <div class="label">{title}</div>
          <div class="rule"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_parchment_table(df_in: pd.DataFrame, height_px: int = 420):
    html = df_in.to_html(index=False, escape=True, classes="parchment-table")
    st.markdown(
        f"""
        <div class="parchment-table-wrap">
          <div class="parchment-table-scroll" style="max-height:{height_px}px;">
            {html}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def top_item_from_semicolon_col(series: pd.Series) -> str:
    items = (
        series.fillna("")
        .apply(lambda x: [i.strip() for i in str(x).split(";") if i.strip()])
        .explode()
    )
    vc = items.value_counts()
    return vc.index[0] if len(vc) else "—"


def ink_etched_line(ax, x, y, color, label=None, seed=0):
    rng = np.random.default_rng(seed)

    line = ax.plot(x, y, color=color, linewidth=2.2, label=label, zorder=3)[0]
    line.set_path_effects(
        [
            pe.Stroke(linewidth=3.6, foreground="#2e2416", alpha=0.18),
            pe.Normal(),
        ]
    )

    y_arr = np.asarray(y, dtype=float)
    jitter = rng.normal(0.0, 0.03, size=len(y_arr))
    rough = np.clip(y_arr + jitter, 0, None)
    ax.plot(x, rough, color=color, linewidth=1.3, alpha=0.28, zorder=2)

    ax.plot(
        x,
        y_arr,
        color="#2e2416",
        linewidth=1.0,
        alpha=0.12,
        linestyle=(0, (2, 4)),
        zorder=1,
    )

    return line


def render_chart_with_compass_plate(fig, svg_opacity=0.14, grain_opacity=0.18):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())
    buf.seek(0)
    png_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    compass_svg = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800">
      <defs>
        <radialGradient id="fade" cx="50%" cy="50%" r="55%">
          <stop offset="0%" stop-color="#6b4f2a" stop-opacity="0.36"/>
          <stop offset="70%" stop-color="#6b4f2a" stop-opacity="0.12"/>
          <stop offset="100%" stop-color="#6b4f2a" stop-opacity="0.00"/>
        </radialGradient>
      </defs>

      <circle cx="400" cy="400" r="290" fill="none" stroke="#6b4f2a" stroke-width="5" opacity="0.45"/>
      <circle cx="400" cy="400" r="235" fill="none" stroke="#6b4f2a" stroke-width="4" opacity="0.35"/>
      <circle cx="400" cy="400" r="170" fill="none" stroke="#6b4f2a" stroke-width="3" opacity="0.28"/>

      <g opacity="0.55">
        <path d="M400 70 L435 330 L400 370 L365 330 Z" fill="#6b4f2a"/>
        <path d="M730 400 L470 435 L430 400 L470 365 Z" fill="#6b4f2a"/>
        <path d="M400 730 L365 470 L400 430 L435 470 Z" fill="#6b4f2a"/>
        <path d="M70 400 L330 365 L370 400 L330 435 Z" fill="#6b4f2a"/>
      </g>

      <circle cx="400" cy="400" r="320" fill="url(#fade)" opacity="0.28"/>

      <g fill="#6b4f2a" opacity="0.28" font-family="Georgia, serif" font-size="34" font-weight="700">
        <text x="400" y="120" text-anchor="middle">N</text>
        <text x="690" y="415" text-anchor="middle">E</text>
        <text x="400" y="715" text-anchor="middle">S</text>
        <text x="110" y="415" text-anchor="middle">W</text>
      </g>
    </svg>
    """
    compass_b64 = base64.b64encode(compass_svg.encode("utf-8")).decode("utf-8")

    grain_svg = """
    <svg xmlns="http://www.w3.org/2000/svg" width="220" height="220" viewBox="0 0 220 220">
      <filter id="n">
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/>
        <feColorMatrix type="matrix"
          values="1 0 0 0 0
                  0 1 0 0 0
                  0 0 1 0 0
                  0 0 0 0.35 0"/>
      </filter>
      <rect width="220" height="220" filter="url(#n)" opacity="0.55"/>
    </svg>
    """
    grain_b64 = base64.b64encode(grain_svg.encode("utf-8")).decode("utf-8")

    html = f"""
    <div style="
      position: relative;
      border-radius: 18px;
      background: rgba(244, 236, 216, 0.82);
      padding: 14px;
      overflow: hidden;
      border: 1px solid rgba(120, 90, 40, 0.26);
      box-shadow:
        0 10px 22px rgba(120, 90, 40, 0.14),
        inset 0 0 0 2px rgba(239, 228, 200, 0.60),
        inset 0 0 0 12px rgba(120, 90, 40, 0.06);
      margin-bottom: 8px;
    ">

      <div style="
        position: absolute;
        inset: 0;
        background-image: url('data:image/svg+xml;base64,{compass_b64}');
        background-repeat: no-repeat;
        background-position: center;
        background-size: 86%;
        opacity: {svg_opacity};
        pointer-events: none;
        z-index: 0;
      "></div>

      <div style="
        position: absolute;
        inset: 0;
        background-image: url('data:image/svg+xml;base64,{grain_b64}');
        background-repeat: repeat;
        opacity: {grain_opacity};
        mix-blend-mode: multiply;
        pointer-events: none;
        z-index: 1;
      "></div>

      <img src="data:image/png;base64,{png_b64}" style="
        position: relative;
        width: 100%;
        height: auto;
        border-radius: 12px;
        z-index: 2;
      "/>
    </div>
    """

    components.html(html, height=520, scrolling=False)


# =========================================================
# 4) DATA LOADING + BASIC DERIVED FIELDS
# =========================================================
DATA_PATH = Path("data/queens_trade_early_modern_1474_1816.csv")


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    d = pd.read_csv(path)
    d["reign_duration"] = d["reign_end"] - d["reign_start"]
    return d


df = load_data(DATA_PATH)


# =========================================================
# 5) SIDEBAR FILTERS — Royal Council
# =========================================================
st.sidebar.markdown("### 👑 The Royal Council")
st.sidebar.caption("Define the realm of inquiry.")
# divider under caption (ONLY this)
st.sidebar.markdown(
    '<div class="council-divider"><span class="sigil">✧</span><div class="line"></div><span class="sigil">✧</span></div>',
    unsafe_allow_html=True
)

if st.sidebar.button("⌁ Clear the Council"):
    for k in [
        "royal_inquiry_text",
        "royal_persona",
        "naval_authority",
        "crown_dominion",
        "sphere_influence",
        "display_mode",
        "queen_selected",
        "compare_a",
        "compare_b",
    ]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()
    
st.sidebar.markdown(
    '<div class="council-divider"><span class="sigil">✧</span><div class="line"></div><span class="sigil">✧</span></div>',
    unsafe_allow_html=True
)    

with st.sidebar.expander("🗝 Council Decrees (Filters)", expanded=True):
    royal_inquiry_text = st.text_input(
        "Royal Inquiry",
        value="",
        key="royal_inquiry_text",
        placeholder="Try: Elizabeth, Atlantic, textiles…",
        help="Searches across all fields (name, empire, regions, exports, ports, policies).",
    )

    queen_options = ["All"] + sorted(df["name"].dropna().unique().tolist())
    royal_persona = st.selectbox(
        "Royal Persona",
        queen_options,
        index=0,
        key="royal_persona",
        help="Click the field and type to jump (e.g., 'e').",
    )

    naval_authority = st.selectbox(
        "Naval Authority",
        ["All", "Yes", "Limited"],
        index=0,
        key="naval_authority",
        help="Filters rulers by maritime orientation in your dataset.",
    )

    empire_options = ["All"] + sorted(df["empire"].dropna().unique().tolist())
    crown_dominion = st.selectbox(
        "Crown & Dominion",
        empire_options,
        index=0,
        key="crown_dominion",
        help="Filter by empire/polity (e.g., England, France, Spain…).",
    )

    all_regions = sorted(
        {r.strip() for s in df["major_trade_regions"].dropna() for r in str(s).split(";") if r.strip()}
    )
    sphere_influence = st.selectbox(
        "Sphere of Influence",
        ["All"] + all_regions,
        index=0,
        key="sphere_influence",
        help="Filter by major trade region (derived from your dataset).",
    )

st.sidebar.markdown(
    '<div class="council-divider"><span class="sigil">✧</span><div class="line"></div><span class="sigil">✧</span></div>',
    unsafe_allow_html=True
)

st.sidebar.markdown('<div class="council-tab">📖 Chronicle Mode</div>', unsafe_allow_html=True)

display_mode = st.sidebar.radio(
    " ",
    ["Story Mode", "Evidence Mode"],
    index=0,
    key="display_mode",
    help="Evidence Mode shows raw fields + provenance placeholders (good digital history practice).",
)


# =========================================================
# 6) APPLY FILTERS
# =========================================================
filtered = df.copy()

if naval_authority != "All":
    filtered = filtered[filtered["maritime_power"] == naval_authority]

if crown_dominion != "All":
    filtered = filtered[filtered["empire"] == crown_dominion]

if sphere_influence != "All":
    filtered = filtered[filtered["major_trade_regions"].str.contains(sphere_influence, case=False, na=False)]

if royal_persona != "All":
    filtered = filtered[filtered["name"] == royal_persona]

if royal_inquiry_text.strip():
    s = royal_inquiry_text.strip()
    filtered = filtered[filtered.apply(lambda row: row.astype(str).str.contains(s, case=False).any(), axis=1)]

# =========================================================
# 7) HEADER (Museum Placard)
# =========================================================
start_year = int(df["reign_start"].min())
end_year = int(df["reign_end"].max())

st.markdown(
    f"""
<div style="
  text-align:center;
  padding: 18px 14px 14px 14px;
  border: 1px solid rgba(120, 90, 40, 0.22);
  border-radius: 16px;
  background: rgba(244, 236, 216, 0.60);
  box-shadow: 0 6px 16px rgba(120, 90, 40, 0.10);
  margin-bottom: 10px;
">
  <div style="font-size:30px;">⚜️</div>

  <div style="font-size:42px; font-weight:800; color:#4a381d;">
    👑 Queens Trade Explorer
  </div>

  <!-- NEW SUBTITLE -->
  <div style="
        font-size:18px;
        margin-top:6px;
        color:#5b4523;
        font-weight:600;
        letter-spacing:0.4px;
  ">
    Modeling early modern global trade governance (15th–19th c.)
  </div>

  <!-- DATE RANGE -->
  <div style="
        font-size:15px;
        color:#6a532f;
        margin-top:6px;
        font-weight:600;
  ">
    {start_year}–{end_year} · Cultural Data Prototype
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.caption(
    "Prototype cultural analytics app: structured historical dataset + filters + comparative insights + governance-overlap visualization."
)


# =========================================================
# 8) TOP KPIs
# =========================================================
k1, k2, k3, k4 = st.columns(4)
k1.metric("Queens (filtered)", len(filtered))
k2.metric("Avg reign (years)", round(filtered["reign_duration"].mean(), 1) if len(filtered) else 0)
k3.metric("Maritime powers (Yes)", int((filtered["maritime_power"] == "Yes").sum()) if len(filtered) else 0)
k4.metric("Empires covered", filtered["empire"].nunique() if len(filtered) else 0)


# =========================================================
# 9) WHOLE TABLE (Collapsible)
# =========================================================
manuscript_header("Whole Table List (Filtered View)", icon="📜")

show_cols = [
    "name",
    "empire",
    "reign_start",
    "reign_end",
    "reign_duration",
    "major_trade_regions",
    "key_ports",
    "key_exports",
    "trade_partners",
    "trade_policy_keywords",
    "maritime_power",
]

with st.expander("📂 Open full dataset (filtered)", expanded=False):
    st.download_button(
        label="⬇️ Download filtered CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="queens_trade_filtered.csv",
        mime="text/csv",
    )
    render_parchment_table(filtered[show_cols].sort_values("reign_duration", ascending=False), height_px=420)


# =========================================================
# 10) MIDDLE LAYOUT: left = selection, right = details
# =========================================================
col1, col2 = st.columns([1.15, 1.85], gap="large")

with col1:
    manuscript_header("Selection List", icon="✦")
    st.caption("Navigate queens based on current filters. Full dataset is above in the expander.")

    sort_choice = st.selectbox(
        "Sort queens by",
        ["reign_duration (desc)", "name (A–Z)", "reign_start (asc)"],
    )

    df_left = filtered.copy()
    if sort_choice == "name (A–Z)":
        df_left = df_left.sort_values("name")
    elif sort_choice == "reign_start (asc)":
        df_left = df_left.sort_values("reign_start")
    else:
        df_left = df_left.sort_values("reign_duration", ascending=False)

    if len(df_left) > 0:
        st.selectbox("Select a queen (searchable)", df_left["name"].tolist(), key="queen_selected")
        render_parchment_table(
            df_left[["name", "empire", "reign_start", "reign_end", "maritime_power"]].head(15),
            height_px=260,
        )
    else:
        st.info("No queens match the current filters.")

with col2:
    manuscript_header("Queen Detail View", icon="👑")

    if len(filtered) == 0:
        st.info("No queens match the current filters. Try adjusting filters.")
    else:
        queen_name = st.session_state.get("queen_selected")
        if not queen_name:
            queen_name = filtered["name"].iloc[0]
            st.session_state["queen_selected"] = queen_name

        q = filtered[filtered["name"] == queen_name].iloc[0]

        q1, q2, q3 = st.columns(3)
        q1.metric("Reign duration", int(q["reign_duration"]))
        q2.metric("Maritime power", str(q["maritime_power"]))
        q3.metric(
            "Trade regions count",
            len([r for r in str(q.get("major_trade_regions", "")).split(";") if r.strip()]),
        )

        st.markdown("")
        left, right = st.columns([1.25, 1], gap="large")

        with left:
            # ✅ Wrap dossier inside parchment-card (so it matches your boxed style)
            dossier_html = f"""
<div class="parchment-card">
  <div class="dossier" style="background: transparent; border: 0; box-shadow: none; padding: 0;">
    <div class="row"><span class="k">Empire:</span> <span class="v">{q.get('empire','')}</span></div>
    <div class="row"><span class="k">Capital:</span> <span class="v">{q.get('capital','')}</span></div>
    <div class="row"><span class="k">Trade Regions:</span> <span class="v">{q.get('major_trade_regions','')}</span></div>
    <div class="row"><span class="k">Key Ports:</span> <span class="v">{q.get('key_ports','')}</span></div>
    <div class="row"><span class="k">Key Exports:</span> <span class="v">{q.get('key_exports','')}</span></div>
    <div class="row"><span class="k">Trade Partners:</span> <span class="v">{q.get('trade_partners','')}</span></div>
    <div class="row"><span class="k">Policy Keywords:</span> <span class="v">{q.get('trade_policy_keywords','')}</span></div>

    <hr style="border:0; border-top:1px solid rgba(120,90,40,0.25); margin:10px 0;">

    <div class="row"><span class="k">Economic Impact:</span></div>
    <div class="row"><span class="v">{q.get('economic_impact_summary','')}</span></div>
  </div>
</div>
"""
            st.markdown(dossier_html, unsafe_allow_html=True)

            if display_mode == "Evidence Mode":
                st.markdown("**Evidence & Provenance (Prototype)**")
                st.caption("Transparency section for digital history credibility.")
                st.markdown(f"- **Record ID (row index):** {int(q.name)}")
                st.markdown(f"- **Portrait URL:** {q.get('portrait_url','')}")
                st.markdown(f"- **Raw regions string:** `{q.get('major_trade_regions','')}`")
                st.markdown(f"- **Raw exports string:** `{q.get('key_exports','')}`")
                st.info("Next: add sources/confidence columns.")

        with right:
            portrait_url = str(q.get("portrait_url", "")).strip()

            try:
                y = int(q.get("reign_start", 0))
            except Exception:
                y = 0

            if y and y < 1600:
                frame_class = "frame-renaissance"
            elif y and y < 1750:
                frame_class = "frame-baroque"
            else:
                frame_class = "frame-wood"

            if portrait_url and portrait_url.lower() not in {"nan", "none", ""}:
                st.markdown(
                    f"""
<div style="display:flex; justify-content:center;">
  <div class="portrait-frame {frame_class}">
    <img class="portrait-img" src="{portrait_url}" alt="Portrait of {q.get('name','')}">
  </div>
</div>

<div class="portrait-name">{q.get('name','')}</div>
<div class="portrait-sub">{q.get('reign_start','')}–{q.get('reign_end','')}</div>
""",
                    unsafe_allow_html=True,
                )
            else:
                st.info("No portrait available for this queen yet.")


# =========================================================
# 11) COMPARE QUEENS
# =========================================================
manuscript_header("Compare Two Queens", icon="⚖️")
st.caption("Comparative structural view of trade systems: identifies overlap, divergence, and governance scale.")

if len(filtered) >= 2:
    cA, cB = st.columns(2, gap="large")
    names = filtered["name"].tolist()

    with cA:
        qA_name = st.selectbox("Queen A", names, index=0, key="compare_a")
    with cB:
        qB_name = st.selectbox("Queen B", names, index=1, key="compare_b")

    qA = filtered[filtered["name"] == qA_name].iloc[0]
    qB = filtered[filtered["name"] == qB_name].iloc[0]

    def split_semicolon(x):
        return {i.strip() for i in str(x).split(";") if i.strip()}

    A_regions = split_semicolon(qA.get("major_trade_regions", ""))
    B_regions = split_semicolon(qB.get("major_trade_regions", ""))
    A_ports = split_semicolon(qA.get("key_ports", ""))
    B_ports = split_semicolon(qB.get("key_ports", ""))
    A_exports = split_semicolon(qA.get("key_exports", ""))
    B_exports = split_semicolon(qB.get("key_exports", ""))

    overlap_regions = sorted(A_regions & B_regions)
    overlap_ports = sorted(A_ports & B_ports)
    overlap_exports = sorted(A_exports & B_exports)

    A_unique_regions = sorted(A_regions - B_regions)
    B_unique_regions = sorted(B_regions - A_regions)

    kA, kB, kC, kD = st.columns(4)
    kA.metric("Reign (A)", int(qA["reign_duration"]))
    kB.metric("Reign (B)", int(qB["reign_duration"]))
    kC.metric("Shared Regions", len(overlap_regions))
    kD.metric("Shared Ports", len(overlap_ports))

    st.markdown("---")
    st.markdown("### Structural Comparison")

    def fmt_list(items):
        return ", ".join(items) if items else "—"

    colS1, colS2, colS3 = st.columns(3, gap="large")

    with colS1:
        st.markdown(
            f"""
            <div class="compare-panel">
                <div class="title">Shared Infrastructure</div>
                <ul>
                    <li><b>Trade regions:</b> {fmt_list(overlap_regions)}</li>
                    <li><b>Ports:</b> {fmt_list(overlap_ports)}</li>
                    <li><b>Exports:</b> {fmt_list(overlap_exports)}</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with colS2:
        st.markdown(
            f"""
            <div class="compare-panel">
                <div class="title">Queen A — Unique</div>
                <ul>
                    <li><b>Regions:</b> {fmt_list(A_unique_regions)}</li>
                    <li><b>Ports:</b> {fmt_list(sorted(A_ports - B_ports))}</li>
                    <li><b>Exports:</b> {fmt_list(sorted(A_exports - B_exports))}</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with colS3:
        st.markdown(
            f"""
            <div class="compare-panel">
                <div class="title">Queen B — Unique</div>
                <ul>
                    <li><b>Regions:</b> {fmt_list(B_unique_regions)}</li>
                    <li><b>Ports:</b> {fmt_list(sorted(B_ports - A_ports))}</li>
                    <li><b>Exports:</b> {fmt_list(sorted(B_exports - A_exports))}</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    interpretation = []
    if len(overlap_regions) == 0:
        interpretation.append("These rulers operated in structurally distinct trade systems.")

    if qA["reign_duration"] > qB["reign_duration"]:
        interpretation.append("Queen A governed longer, potentially enabling deeper trade consolidation.")
    elif qB["reign_duration"] > qA["reign_duration"]:
        interpretation.append("Queen B governed longer, suggesting sustained trade continuity.")

    if interpretation:
        st.markdown("### Interpretive Insight")
        st.markdown(" ".join(interpretation))
else:
    st.info("Need at least two queens in the filtered dataset to compare.")


# =========================================================
# 12) QUICK INSIGHTS
# =========================================================
manuscript_header("Quick Insights", icon="✧")

if len(filtered) == 0:
    st.warning("No results for current filters.")
else:
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**🌍 Top Regions**")
        regions_series = (
            filtered["major_trade_regions"]
            .fillna("")
            .apply(lambda x: [r.strip() for r in str(x).split(";") if r.strip()])
            .explode()
        )
        regions_df = regions_series.value_counts().head(5).reset_index()
        regions_df.columns = ["Region", "Count"]
        render_parchment_table(regions_df, height_px=220)

    with c2:
        st.markdown("**📦 Top Exports**")
        exports_series = (
            filtered["key_exports"]
            .fillna("")
            .apply(lambda x: [e.strip() for e in str(x).split(";") if e.strip()])
            .explode()
        )
        exports_df = exports_series.value_counts().head(5).reset_index()
        exports_df.columns = ["Export", "Count"]
        render_parchment_table(exports_df, height_px=220)

    with c3:
        st.markdown("**🚢 Maritime Split**")
        mar_df = filtered["maritime_power"].value_counts().reset_index()
        mar_df.columns = ["Maritime Power", "Count"]
        render_parchment_table(mar_df, height_px=180)


# =========================================================
# 13) HIGHLIGHTS
# =========================================================
manuscript_header("Highlights from the Filtered Dataset", icon="✦")

top_region = top_item_from_semicolon_col(filtered["major_trade_regions"]) if len(filtered) else "—"
top_export = top_item_from_semicolon_col(filtered["key_exports"]) if len(filtered) else "—"
top_empire = filtered["empire"].value_counts().index[0] if len(filtered) else "—"

if len(filtered) and "key_ports" in filtered.columns:
    ports = (
        filtered["key_ports"]
        .fillna("")
        .apply(lambda x: [p.strip() for p in str(x).split(";") if p.strip()])
        .explode()
    )
    unique_ports = int(ports.nunique()) if len(ports) else 0
else:
    unique_ports = 0

h1, h2, h3, h4 = st.columns(4)
h1.metric("Top Trade Region", top_region)
h2.metric("Top Export", top_export)
h3.metric("Top Empire", top_empire)
h4.metric("Unique Ports", unique_ports)


# =========================================================
# 14) CHART: Trade Governance Over Time
# =========================================================
manuscript_header("Trade Governance Over Time", icon="🧭")

mode = st.radio(
    "View mode",
    ["Show Maritime vs Total", "Show Only Maritime Powers", "Show by Empire"],
    horizontal=True,
)

if len(filtered) == 0:
    st.info("No data to plot for current filters.")
else:
    y_min = int(filtered["reign_start"].min())
    y_max = int(filtered["reign_end"].max())
    years = list(range(y_min, y_max + 1))

    total_active = []
    maritime_active = []

    for y in years:
        active = filtered[(filtered["reign_start"] <= y) & (filtered["reign_end"] >= y)]
        total_active.append(len(active))
        maritime_active.append(int((active["maritime_power"] == "Yes").sum()))

    timeline_df = pd.DataFrame(
        {"Year": years, "Total Active Queens": total_active, "Maritime Active Queens": maritime_active}
    )

    fig, ax = plt.subplots(figsize=(10.5, 4.2))
    fig.patch.set_facecolor("#f4ecd8")
    ax.set_facecolor("#f4ecd8")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#8a6d3b")
    ax.spines["bottom"].set_color("#8a6d3b")
    ax.tick_params(colors="#5a4a2f")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.22, color="#8a6d3b")
    ax.set_xlabel("Year", color="#5a4a2f", fontname="Georgia")
    ax.set_ylabel("Count of rulers active", color="#5a4a2f", fontname="Georgia")

    span = y_max - y_min
    step = 25 if span <= 250 else 50
    ticks = list(range((y_min // step) * step, y_max + 1, step))
    ticks = [t for t in ticks if y_min <= t <= y_max]
    ax.set_xticks(ticks)

    insight_text = ""

    if mode == "Show Maritime vs Total":
        ink_etched_line(ax, timeline_df["Year"], timeline_df["Total Active Queens"], color="#6b4f2a", label="Total queens active", seed=11)
        ink_etched_line(ax, timeline_df["Year"], timeline_df["Maritime Active Queens"], color="#b08a3a", label="Maritime-power queens active", seed=22)

        ax.fill_between(timeline_df["Year"], timeline_df["Maritime Active Queens"], 0, color="#b08a3a", alpha=0.08)

        ratio = [(m / t) if t > 0 else 0.0 for t, m in zip(total_active, maritime_active)]
        peak_idx = int(pd.Series(ratio).idxmax())
        peak_year = int(timeline_df.loc[peak_idx, "Year"])
        peak_total = int(timeline_df.loc[peak_idx, "Total Active Queens"])
        peak_mar = int(timeline_df.loc[peak_idx, "Maritime Active Queens"])
        peak_pct = round((peak_mar / peak_total) * 100, 1) if peak_total > 0 else 0.0

        ax.scatter([peak_year], [peak_mar], color="#4a381d", s=40, zorder=4)
        ax.text(peak_year, peak_mar + 0.15, f"peak maritime share: {peak_pct}% ({peak_year})", color="#4a381d", fontsize=10, fontname="Georgia")

        ax.set_title("Maritime dominance vs total governance (year-by-year overlap)", color="#4a381d", fontname="Georgia")

        leg = ax.legend(frameon=True)
        for t in leg.get_texts():
            t.set_color("#4a381d")
            t.set_fontname("Georgia")
        leg.get_frame().set_facecolor("#efe4c8")
        leg.get_frame().set_edgecolor("#d8c9a6")

        insight_text = f"**Key insight:** Peak maritime dominance occurs around **{peak_year}**, where **{peak_mar}/{peak_total}** active rulers are maritime powers (**{peak_pct}%**)."

    elif mode == "Show Only Maritime Powers":
        ink_etched_line(ax, timeline_df["Year"], timeline_df["Maritime Active Queens"], color="#b08a3a", label="Maritime-power queens active", seed=33)
        ax.fill_between(timeline_df["Year"], timeline_df["Maritime Active Queens"], 0, color="#b08a3a", alpha=0.10)

        peak_idx = int(timeline_df["Maritime Active Queens"].idxmax())
        peak_year = int(timeline_df.loc[peak_idx, "Year"])
        peak_val = int(timeline_df.loc[peak_idx, "Maritime Active Queens"])

        ax.scatter([peak_year], [peak_val], color="#4a381d", s=40, zorder=4)
        ax.text(peak_year, peak_val + 0.15, f"peak: {peak_val} ({peak_year})", color="#4a381d", fontsize=10, fontname="Georgia")
        ax.set_title("Maritime-power rulers active over time", color="#4a381d", fontname="Georgia")

        insight_text = f"**Key insight:** Maritime-power activity peaks around **{peak_year}** with **{peak_val}** maritime rulers active."

    else:
        top_empires = filtered["empire"].value_counts().head(3).index.tolist()
        empire_colors = ["#6b4f2a", "#b08a3a", "#8a6d3b"]

        for i, emp in enumerate(top_empires):
            emp_df = filtered[filtered["empire"] == emp]
            emp_counts = []
            for y in years:
                active_emp = emp_df[(emp_df["reign_start"] <= y) & (emp_df["reign_end"] >= y)]
                emp_counts.append(len(active_emp))

            ink_etched_line(ax, years, emp_counts, color=empire_colors[i % len(empire_colors)], label=str(emp), seed=100 + i)

        ax.set_title("Active rulers over time by empire (top 3 in current filters)", color="#4a381d", fontname="Georgia")

        leg = ax.legend(frameon=True)
        for t in leg.get_texts():
            t.set_color("#4a381d")
            t.set_fontname("Georgia")
        leg.get_frame().set_facecolor("#efe4c8")
        leg.get_frame().set_edgecolor("#d8c9a6")

        insight_text = "**Key insight:** This view compares governance overlap by empire. Use filters to focus on one region or trade system."

    plt.tight_layout()
    render_chart_with_compass_plate(fig, svg_opacity=0.14, grain_opacity=0.18)

    st.caption(
        "These curves show **how many rulers are active in each year** based on reign overlap "
        "(not trade volume). It’s a governance-intensity proxy for comparing historical systems."
    )
    if insight_text:
        st.markdown(insight_text)
        
        
# =========================================================
# 15) ABOUT
# =========================================================        
manuscript_header("Next Up (Roadmap)", icon="🧭")

st.markdown(
    """    
Queens Trade Explorer (1474–1816) is a cultural data prototype that models early modern trade governance 
as a structured, queryable system rather than a static narrative.

The project translates historical knowledge into a relational-style dataset centered on rulers as entities,
with trade regions, ports, exports, partners, and policy signals represented as structured attributes.
It enables comparative analysis, faceted exploration, and temporal overlap modeling.

This prototype demonstrates how historical systems can be abstracted into data models that support:
- Pattern recognition  
- Comparative reasoning  
- Governance-intensity analysis  
- Structured interpretive transparency  

It sits at the intersection of history, data engineering, and interactive systems design
    
This prototype is designed as a foundation for a larger cultural systems platform.
Planned extensions focus on credibility, structural modeling, and immersive interfaces.
"""
)

r1, r2, r3 = st.columns(3, gap="large")

with r1:
    st.markdown(
        """
        <div class="parchment-card">
        <h4>📚 Data & Credibility</h4>
        <ul>
            <li>Field-level provenance (source, citation, confidence score)</li>
            <li>Versioned dataset tracking interpretive updates</li>
            <li>Schema documentation + public data package</li>
            <li>Exportable structured research dossiers</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r2:
    st.markdown(
        """
        <div class="parchment-card">
        <h4>🌐 Structural Modeling</h4>
        <ul>
            <li>Interactive trade network graph (ports ↔ regions ↔ partners)</li>
            <li>Centrality metrics & governance intensity index</li>
            <li>Similarity search between rulers (vector-based comparison)</li>
            <li>Clustering of trade system archetypes</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r3:
    st.markdown(
        """
        <div class="parchment-card">
        <h4>🤖 Immersive & AI Layer</h4>
        <ul>
            <li>AI-assisted period-style portrait synthesis (clearly labeled reconstructions)</li>
            <li>“Living Manuscript Gallery” mode with subtle animated portraits</li>
            <li>Natural-language query interface</li>
            <li>Policy-language summarization from structured fields</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )