
import pandas as pd
import folium


# Load dataset
df = pd.read_csv("../data/queens_trade_early_modern_1474_1816.csv")

# Create map WITHOUT default tiles (we'll add vintage options)
m = folium.Map(location=[30, 20], zoom_start=3, tiles=None)

# 1) Vintage-ish terrain
folium.TileLayer(
    "OpenTopoMap",
    name="Vintage Terrain (OpenTopoMap)",
    control=True
).add_to(m)

# 2) Clean parchment-like (light)
folium.TileLayer(
    "CartoDB positron",
    name="Clean Light (Positron)",
    control=True
).add_to(m)

# 3) Dark ink style (looks like old atlas print)
folium.TileLayer(
    "CartoDB dark_matter",
    name="Ink Dark (Dark Matter)",
    control=True
).add_to(m)

# Title
title_html = """
<div style="
position: fixed;
top: 10px; left: 50%;
transform: translateX(-50%);
z-index: 9999;
background: rgba(245, 241, 230, 0.92);
padding: 8px 14px;
border: 1px solid rgba(0,0,0,0.25);
border-radius: 10px;
font-family: Georgia, serif;
">
<b>Queens Who Shaped Global Trade Networks (1474_1816)</b>
</div>
"""
m.get_root().html.add_child(folium.Element(title_html))

# Feature groups (so users can toggle)
maritime_fg = folium.FeatureGroup(name="Maritime Powers (Yes)", show=True)
limited_fg = folium.FeatureGroup(name="Limited / Mostly Land Power", show=True)
routes_fg = folium.FeatureGroup(name="Trade Corridors", show=True)

all_points = []

for _, row in df.iterrows():
    lat, lon = float(row["latitude"]), float(row["longitude"])
    all_points.append([lat, lon])

    popup_text = f"""
    <div style="font-family: Georgia, serif;">
      <b style="font-size:14px;">{row['name']}</b><br>
      <span>Empire: {row['empire']}</span><br>
      <span>Reign: {row['reign_start']} – {row['reign_end']}</span><br>
      <span><b>Trade Regions:</b> {row['major_trade_regions']}</span><br>
      <span><b>Exports:</b> {row['key_exports']}</span><br>
      <hr style="margin:6px 0;">
      <span>{row['economic_impact_summary']}</span>
    </div>
    """

    icon_color = "darkpurple" if str(row["maritime_power"]).strip() == "Yes" else "cadetblue"

    marker = folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_text, max_width=340),
        tooltip=row["name"],
        icon=folium.Icon(color=icon_color, icon="info-sign")
    )

    if str(row["maritime_power"]).strip() == "Yes":
        marker.add_to(maritime_fg)
    else:
        marker.add_to(limited_fg)

    # Trade route lines
    if pd.notna(row["trade_route_coordinates"]):
        coords = []
        for point in str(row["trade_route_coordinates"]).split("|"):
            p_lat, p_lon = point.split(",")
            coords.append([float(p_lat), float(p_lon)])
            all_points.append([float(p_lat), float(p_lon)])

        folium.PolyLine(
            locations=coords,
            color="#8B4513",   # earthy brown
            weight=3,
            opacity=0.65
        ).add_to(routes_fg)

# Add layers
maritime_fg.add_to(m)
limited_fg.add_to(m)
routes_fg.add_to(m)

# Legend
legend_html = """
<div style="
position: fixed;
bottom: 20px; left: 20px;
z-index: 9999;
background: rgba(245, 241, 230, 0.92);
padding: 10px 12px;
border: 1px solid rgba(0,0,0,0.25);
border-radius: 10px;
font-family: Georgia, serif;
font-size: 13px;
">
<div><b>Legend</b></div>
<div style="margin-top:6px;">🟣 Maritime power = Yes</div>
<div>🔵 Limited / land-focused</div>
<div style="margin-top:6px;">🟤 Trade corridor (simplified)</div>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Controls
folium.LayerControl(collapsed=False).add_to(m)

# Auto-fit bounds
if all_points:
    m.fit_bounds(all_points, padding=(20, 20))

m.save("queens_trade_map.html")
print("Upgraded premium map saved: queens_trade_map.html")