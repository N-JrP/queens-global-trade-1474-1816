# 👑 Queens Global Trade Explorer (1474–1816)

**Early Modern Global Trade Governance (15th–19th century)**  
A digital humanities prototype combining structured historical data, interactive filtering, and governance-overlap visualization.

---

## 🌍 Project Overview

This project transforms narrative historical information about queens and trade systems into a structured dataset and interactive analytical interface.

It demonstrates how historical governance, maritime orientation, and trade infrastructure can be modeled computationally and explored dynamically.

The system includes:

- A Streamlit data explorer
- A Comparative governance module
- A Temporal overlap visualization
- An optional interactive trade corridor map (Folium)

---

## 🔎 Key Features

### 👑 Royal Council Filtering
- Free-text global search
- Structured filtering (maritime power, empire, region)
- Persona-based queen selection
- Story Mode vs Evidence Mode toggle

### 📜 Queen Dossier View
- Trade regions
- Key ports
- Major exports
- Trade partners
- Policy keywords
- Economic impact summary

### ⚖️ Structural Comparison Engine
Compare two rulers:
- Shared trade regions
- Shared ports
- Shared exports
- Unique governance domains

### 🧭 Trade Governance Timeline
Visualizes how many rulers were active per year (1474–1816), including maritime dominance comparison.

This functions as a governance-intensity proxy, not trade volume.

---

## 🗺️ Interactive Trade Map (Optional Module)

Built with Folium.

Features:
- Toggle maritime vs land-oriented rulers
- Simplified trade corridors
- Vintage and atlas-style map themes
- Auto-fit bounds for historical network scope

---

## 🧠 What This Demonstrates

This project highlights:

- Historical data modeling
- Semi-structured data transformation
- Cultural analytics
- Interactive UI development (Streamlit)
- Governance overlap abstraction
- Digital humanities systems thinking

It represents a bridge between historical inquiry and computational design.

---

## 📂 Project Structure

assets/      → background manuscript-style map image  
data/        → structured CSV dataset  
map/         → interactive Folium trade map  
notebooks/   → exploratory data analysis  
app.py       → main Streamlit application  

---

## ▶️ How to Run Locally

Install dependencies:

pip install -r requirements.txt

Run the Streamlit app:

streamlit run app.py

To generate the trade map:

python map/interactive_trade_map.py

Or open:

map/queens_trade_map.html

---

## 📊 Data Coverage

- Time span: 1474–1816
- Regions, exports, and ports are semi-structured (semicolon-separated)
- Trade corridors represented as simplified polylines
- Maritime power classification included in dataset

---

## 🚀 Roadmap / Future Extensions

- Network graph visualization (ports ↔ regions ↔ empires)
- Provenance fields (sources + confidence scoring)
- Animated “living portrait” UI enhancement
- Embedded interactive map inside Streamlit
- Timeline slider exploration
- API layer for dataset access

---

## 📌 Purpose

This is a prototype demonstrating how historical systems can be:

1. Structured  
2. Modeled  
3. Visualized  
4. Compared  
5. Interacted with computationally  

Designed for roles at the intersection of:
- Digital Humanities
- Cultural Analytics
- Data Visualization
- Historical Systems Modeling
- History + Technology

---

If you are reviewing this for hiring or collaboration, this project represents a working example of transforming historical narrative into computational infrastructure.
