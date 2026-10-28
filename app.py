"""
========================================================================================
Inventory & Supply Chain Procurement Optimization Dashboard (ProcureOptix Enterprise)
----------------------------------------------------------------------------------------
Domain: Mechanical & Manufacturing Operations / Supply Chain Data Engineering
Stack: Python, Streamlit, SQLite (In-Memory with StaticPool), SQLAlchemy, Pandas, NumPy, Plotly
Features: Dynamic ROP, EOQ Modeling, ABC Pareto Analysis, Real-time SQL Engine, ERP Export
========================================================================================
"""

import sqlite3
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

# ======================================================================================
# 1. ENTERPRISE UI CONFIGURATION & HIGH-END MODERN CSS
# ======================================================================================
st.set_page_config(
    page_title="ProcureOptix | Enterprise Supply Chain & Inventory Optimization",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom UI Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }

    /* Executive Glassmorphic Header */
    .dashboard-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #090d16 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px 30px;
        color: #ffffff;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    .dashboard-title {
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0;
        background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .dashboard-subtitle {
        font-size: 0.88rem;
        color: #94a3b8;
        margin-top: 6px;
        font-weight: 400;
    }
    .badge-bar {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    .header-pill {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.14);
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.78rem;
        color: #e2e8f0;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #10b981;
    }

    /* Executive KPI Metric Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        transition: all 0.25s ease-in-out;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.09);
        border-color: #cbd5e1;
    }
    .metric-top-bar {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }
    .bar-blue { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
    .bar-red { background: linear-gradient(90deg, #ef4444, #f87171); }
    .bar-green { background: linear-gradient(90deg, #10b981, #34d399); }
    .bar-purple { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
    .bar-amber { background: linear-gradient(90deg, #f59e0b, #fbbf24); }

    .metric-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748b;
        margin-top: 4px;
        margin-bottom: 6px;
    }
    .metric-val {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
    }
    .metric-footer {
        font-size: 0.76rem;
        margin-top: 6px;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .text-danger { color: #dc2626 !important; font-weight: 600; }
    .text-success { color: #16a34a !important; font-weight: 600; }

    /* Custom Badges */
    .risk-badge-high {
        background: #fee2e2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.75rem;
        border: 1px solid #fca5a5;
        display: inline-block;
    }
    .risk-badge-safe {
        background: #dcfce7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.75rem;
        border: 1px solid #86efac;
        display: inline-block;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        padding: 8px 18px;
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        color: #64748b;
        font-size: 0.88rem;
    }
    .stTabs [aria-selected="true"] {
        color: #2563eb !important;
        background-color: #eff6ff !important;
        border-bottom: 2px solid #2563eb;
    }
</style>
""", unsafe_allow_html=True)


# ======================================================================================
# 2. DATA GENERATION & ARCHITECTURE (REALISTIC MANUFACTURING TAXONOMY)
# ======================================================================================
@st.cache_data(show_spinner=False)
def generate_master_procurement_records(num_records: int = 550, seed: int = 42) -> pd.DataFrame:
    """
    Generates 500+ realistic manufacturing procurement logs based on authentic
    mechanical component specifications and operations research principles.
    """
    np.random.seed(seed)
    
    # Authentic mechanical component catalog with standard engineering specifications
    component_catalog = {
        "Mechanical Fasteners": [
            ("M12x50 High-Tensile Hex Bolt Gr 8.8", 14.0, 48.0),
            ("DIN 985 M10 Prevailing Torque Lock Nut", 8.0, 32.0),
            ("M16 Hardened Structural Flat Washer", 6.0, 22.0),
            ("Socket Head Cap Screw M8x35 Stainless A2", 18.0, 65.0)
        ],
        "Hydraulics & Seals": [
            ("Double-Acting Hydraulic Cylinder 50mm Bore", 210.0, 580.0),
            ("NBR 70 Shore Hydraulic O-Ring Seal Kit", 35.0, 110.0),
            ("300 Bar High-Pressure Directional Valve", 160.0, 440.0),
            ("Reinforced Hydraulic Hose Assembly 1/2-inch", 75.0, 220.0)
        ],
        "Bearings & Transmission": [
            ("SKF Deep Groove Ball Bearing 6205-2RS", 85.0, 240.0),
            ("Timken Tapered Roller Bearing 32008X", 140.0, 390.0),
            ("Synchronous HTD Timing Belt 8M-1200", 65.0, 180.0),
            ("Self-Aligning Pillow Block Bearing UCP206", 110.0, 310.0)
        ],
        "Machined Castings": [
            ("Ductile Iron Pump Housing Casting Grade 65-45-12", 280.0, 890.0),
            ("4140 Alloy Steel CNC Machined Drive Shaft", 220.0, 680.0),
            ("Die-Cast Aluminum Motor End-Shield", 150.0, 460.0),
            ("Phosphor Bronze Machined Bushing 35mm ID", 95.0, 290.0)
        ],
        "Sensors & Actuators": [
            ("M18 Shielded Inductive Proximity Sensor PNP", 120.0, 340.0),
            ("Type-K Heavy-Duty Industrial Thermocouple", 85.0, 260.0),
            ("NEMA 34 High-Torque Hybrid Stepper Motor", 250.0, 780.0),
            ("Rotary Incremental Optical Encoder 1024 PPR", 190.0, 620.0)
        ],
        "Pneumatic Components": [
            ("5/2-Way Solenoid Pilot Valve 24V DC", 75.0, 240.0),
            ("Compact Guided Cylinder 25mm Bore 50mm Stroke", 115.0, 340.0),
            ("Air Filter Regulator Lubricator (FRL) Unit", 95.0, 280.0),
            ("Push-in One-Touch Pneumatic Fittings 10mm (Pack)", 45.0, 130.0)
        ]
    }
    
    suppliers = ["Alpha", "Beta", "Gamma", "Delta"]
    categories = list(component_catalog.keys())
    
    records = []
    for i in range(1, num_records + 1):
        category = np.random.choice(categories)
        parts = component_catalog[category]
        part_name, min_price, max_price = parts[np.random.randint(0, len(parts))]
        
        prefix = category[:3].upper()
        sku_id = f"SKU-{prefix}-{1000 + i}"
        
        supplier = np.random.choice(suppliers, p=[0.28, 0.26, 0.24, 0.22])
        
        # Lead time strictly 3 to 20 days as required
        if supplier == "Alpha":
            lead_time = int(np.clip(np.random.normal(8, 2.5), 3, 20))
        elif supplier == "Beta":
            lead_time = int(np.clip(np.random.normal(12, 3.5), 3, 20))
        elif supplier == "Gamma":
            lead_time = int(np.clip(np.random.normal(14, 3.0), 3, 20))
        else: # Delta
            lead_time = int(np.clip(np.random.normal(11, 3.5), 3, 20))
            
        daily_demand = int(np.random.randint(5, 115))
        safety_stock = int(np.random.randint(30, 320))
        
        # Reorder Point strictly: (Lead_Time_Days * Daily_Demand) + Safety_Stock
        reorder_point = (lead_time * daily_demand) + safety_stock
        
        # Realistic manufacturing unit cost in USD
        base_unit_cost_usd = round(float(np.random.uniform(min_price, max_price)), 2)
        
        # Model ~27% items under high-risk stockout deficit condition
        is_high_risk = np.random.rand() < 0.27
        if is_high_risk:
            current_stock = int(reorder_point * np.random.uniform(0.35, 0.94))
        else:
            current_stock = int(reorder_point * np.random.uniform(1.10, 2.40))
            
        # Stockout Risk: 'High Risk' if Current_Stock < Reorder_Point else 'Safe'
        stockout_risk = "High Risk" if current_stock < reorder_point else "Safe"
        
        # Operations Research: Wilson's Economic Order Quantity (EOQ)
        annual_demand = daily_demand * 300
        order_cost_s = 50.0  # $50 standard PO processing cost
        holding_cost_h = max(1.0, 0.20 * base_unit_cost_usd)  # 20% carrying rate
        eoq = int(np.round(np.sqrt((2 * annual_demand * order_cost_s) / holding_cost_h)))
        
        # Sizing and metrics
        deficit_qty = max(0, reorder_point - current_stock)
        suggested_order_qty = max(eoq, int((reorder_point * 1.5) - current_stock)) if current_stock < reorder_point else 0
        runway_days = round(current_stock / daily_demand, 1) if daily_demand > 0 else 0.0

        records.append({
            "SKU_ID": sku_id,
            "Part_Description": part_name,
            "Category": category,
            "Supplier": supplier,
            "Lead_Time_Days": lead_time,
            "Base_Cost_USD": base_unit_cost_usd,
            "Daily_Demand": daily_demand,
            "Current_Stock": current_stock,
            "Safety_Stock": safety_stock,
            "Reorder_Point": reorder_point,
            "Stockout_Risk": stockout_risk,
            "Deficit_Quantity": deficit_qty,
            "EOQ_Units": eoq,
            "Suggested_Order_Qty": suggested_order_qty,
            "Runway_Days": runway_days
        })
        
    df = pd.DataFrame(records)
    
    # Pareto ABC Analysis: Rank by annual dollar volume (Daily_Demand * 300 * Base_Cost_USD)
    df["Annual_Volume_USD"] = df["Daily_Demand"] * 300 * df["Base_Cost_USD"]
    df = df.sort_values(by="Annual_Volume_USD", ascending=False).reset_index(drop=True)
    df["Cumulative_Value"] = df["Annual_Volume_USD"].cumsum()
    total_val = df["Annual_Volume_USD"].sum()
    df["Cumulative_Share"] = df["Cumulative_Value"] / total_val
    
    def assign_abc(share):
        if share <= 0.70:
            return "Class A (High Value)"
        elif share <= 0.90:
            return "Class B (Moderate)"
        else:
            return "Class C (Low Value)"
            
    df["ABC_Class"] = df["Cumulative_Share"].apply(assign_abc)
    df = df.sort_values(by="SKU_ID").reset_index(drop=True)
    return df


# ======================================================================================
# 3. RELATIONAL SQLITE IN-MEMORY ENGINE (WITH STATICPOOL)
# ======================================================================================
@st.cache_resource(show_spinner=False)
def get_sqlite_engine():
    """
    Creates a singleton in-memory SQLite engine with StaticPool.
    StaticPool guarantees connection persistence and eliminates 'no such table' errors.
    """
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )


def sync_database_table(df: pd.DataFrame, engine):
    """Refreshes the 'procurement_inventory' table in the active SQLite database."""
    df.to_sql("procurement_inventory", con=engine, if_exists="replace", index=False)


def run_sql_query(query: str, engine) -> pd.DataFrame:
    """Executes SQL query against SQLite database and returns result DataFrame."""
    with engine.connect() as conn:
        return pd.read_sql_query(query, conn)


# ======================================================================================
# 4. DATA INITIALIZATION & SESSION CONTROLS
# ======================================================================================
if "seed_value" not in st.session_state:
    st.session_state.seed_value = 42

master_raw_df = generate_master_procurement_records(num_records=550, seed=st.session_state.seed_value)
db_engine = get_sqlite_engine()

# ======================================================================================
# 5. SIDEBAR: OPERATIONAL FILTERS & DUAL CURRENCY ENGINE
# ======================================================================================
with st.sidebar:
    st.markdown("### ⚙️ Procurement Controls")
    
    # Currency Selection (With realistic Indian Industry vs USD conversion)
    currency_choice = st.selectbox(
        "💱 Currency Representation",
        options=["INR (₹) - Indian Industry", "USD ($) - Global USD"],
        index=0,
        help="Converts all unit costs, stock valuations, and expedite budgets accurately."
    )
    
    is_inr = "INR" in currency_choice
    curr_symbol = "₹" if is_inr else "$"
    exchange_rate = 83.0 if is_inr else 1.0  # 1 USD = 83.0 INR

    st.markdown("---")
    
    # Supplier Filter
    all_suppliers = sorted(list(master_raw_df["Supplier"].unique()))
    select_all_supp = st.checkbox("Select All Suppliers", value=True)
    
    if select_all_supp:
        selected_suppliers = st.multiselect("Supplier Partner", options=all_suppliers, default=all_suppliers)
    else:
        selected_suppliers = st.multiselect("Supplier Partner", options=all_suppliers, default=["Alpha", "Beta"])
        
    if not selected_suppliers:
        selected_suppliers = all_suppliers
        st.info("ℹ️ Defaulted to all suppliers (none selected).")

    # Risk Filter
    risk_choice = st.radio(
        "🛡️ Stockout Risk Level",
        options=["All Items", "High Risk Only", "Safe Items Only"],
        index=0
    )

    # Component Category Filter
    all_categories = sorted(list(master_raw_df["Category"].unique()))
    selected_categories = st.multiselect("🏷️ Category Classification", options=all_categories, default=all_categories)
    if not selected_categories:
        selected_categories = all_categories

    # Lead Time Slider
    min_lt, max_lt = int(master_raw_df["Lead_Time_Days"].min()), int(master_raw_df["Lead_Time_Days"].max())
    selected_lt = st.slider("⏱️ Lead Time Range (Days)", min_value=min_lt, max_value=max_lt, value=(min_lt, max_lt))

    st.markdown("---")
    st.markdown("### 🧪 Disruption Simulation")
    lead_time_shock = st.slider(
        "Simulate Lead Time Shock (%)",
        min_value=0,
        max_value=60,
        value=0,
        step=5,
        help="Simulates port delays or vendor bottlenecks by scaling lead times."
    )

    st.markdown("---")
    if st.button("🔄 Regenerate Dataset", use_container_width=True):
        st.session_state.seed_value = np.random.randint(100, 99999)
        st.cache_data.clear()
        st.rerun()

# Build Active Working DataFrame with Currency & Disruption applied
working_df = master_raw_df.copy()

# Apply Currency Conversion
working_df["Unit_Cost"] = (working_df["Base_Cost_USD"] * exchange_rate).round(2)
working_df["Inventory_Value"] = (working_df["Current_Stock"] * working_df["Unit_Cost"]).round(2)
working_df["Urgent_Reorder_Cost"] = (working_df["Deficit_Quantity"] * working_df["Unit_Cost"]).round(2)

# Apply Disruption Shock if activated
if lead_time_shock > 0:
    shock_mult = 1.0 + (lead_time_shock / 100.0)
    working_df["Lead_Time_Days"] = (working_df["Lead_Time_Days"] * shock_mult).round().astype(int)
    working_df["Reorder_Point"] = (working_df["Lead_Time_Days"] * working_df["Daily_Demand"]) + working_df["Safety_Stock"]
    working_df["Stockout_Risk"] = np.where(working_df["Current_Stock"] < working_df["Reorder_Point"], "High Risk", "Safe")
    working_df["Deficit_Quantity"] = np.maximum(0, working_df["Reorder_Point"] - working_df["Current_Stock"])
    working_df["Suggested_Order_Qty"] = np.maximum(working_df["EOQ_Units"], (working_df["Reorder_Point"] * 1.5) - working_df["Current_Stock"]).round().astype(int)
    working_df["Urgent_Reorder_Cost"] = (working_df["Deficit_Quantity"] * working_df["Unit_Cost"]).round(2)

# Always keep SQLite Database fully synchronized with the active working DataFrame
sync_database_table(working_df, db_engine)

# Filtered View for UI
filtered_df = working_df[
    (working_df["Supplier"].isin(selected_suppliers)) &
    (working_df["Category"].isin(selected_categories)) &
    (working_df["Lead_Time_Days"] >= selected_lt[0]) &
    (working_df["Lead_Time_Days"] <= selected_lt[1])
].copy()

if risk_choice == "High Risk Only":
    filtered_df = filtered_df[filtered_df["Stockout_Risk"] == "High Risk"]
elif risk_choice == "Safe Items Only":
    filtered_df = filtered_df[filtered_df["Stockout_Risk"] == "Safe"]


# ======================================================================================
# 6. EXECUTIVE HEADER & METRIC KPI CARDS
# ======================================================================================
st.markdown(f"""
<div class="dashboard-header">
    <div>
        <h1 class="dashboard-title">📦 Inventory & Supply Chain Procurement Optimization Dashboard</h1>
        <div class="dashboard-subtitle">
            Manufacturing Operations Analytics & Warehouse Decision Support System | SQLite In-Memory Engine
        </div>
    </div>
    <div class="badge-bar">
        <span class="header-pill"><span class="pulse-dot"></span> In-Memory SQLite Online</span>
        <span class="header-pill">💱 Currency: {curr_symbol} ({'INR' if is_inr else 'USD'})</span>
        <span class="header-pill">📊 550 Procurement Logs</span>
        <span class="header-pill">⚡ Dynamic ROP + EOQ</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Calculate High-Impact KPIs
total_skus = len(filtered_df)
high_risk_count = (filtered_df["Stockout_Risk"] == "High Risk").sum()
safe_count = (filtered_df["Stockout_Risk"] == "Safe").sum()
high_risk_pct = round((high_risk_count / total_skus * 100), 1) if total_skus > 0 else 0.0
avg_lead_time = round(filtered_df["Lead_Time_Days"].mean(), 1) if total_skus > 0 else 0.0
total_inventory_val = filtered_df["Inventory_Value"].sum() if total_skus > 0 else 0.0
urgent_capital_needed = filtered_df[filtered_df["Stockout_Risk"] == "High Risk"]["Urgent_Reorder_Cost"].sum() if total_skus > 0 else 0.0

# Render Sleek Metric Cards
kpi_c1, kpi_c2, kpi_c3, kpi_c4, kpi_c5 = st.columns(5)

with kpi_c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-top-bar bar-blue"></div>
        <div class="metric-label">Total Monitored SKUs</div>
        <div class="metric-val">{total_skus:,}</div>
        <div class="metric-footer">Active Manufacturing Items</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-top-bar bar-red"></div>
        <div class="metric-label">High Risk Items</div>
        <div class="metric-val" style="color: #dc2626;">{high_risk_count:,}</div>
        <div class="metric-footer text-danger">⚠️ {high_risk_pct}% Stockout Hazard</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-top-bar bar-green"></div>
        <div class="metric-label">Safe Buffer SKUs</div>
        <div class="metric-val" style="color: #16a34a;">{safe_count:,}</div>
        <div class="metric-footer text-success">✓ Stock ≥ Reorder Point</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-top-bar bar-amber"></div>
        <div class="metric-label">Avg Lead Time</div>
        <div class="metric-val">{avg_lead_time} <span style="font-size: 1rem; color: #64748b; font-weight: 600;">Days</span></div>
        <div class="metric-footer">Across Active Suppliers</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_c5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-top-bar bar-purple"></div>
        <div class="metric-label">Urgent Expedite Budget</div>
        <div class="metric-val" style="color: #2563eb;">{curr_symbol}{urgent_capital_needed:,.0f}</div>
        <div class="metric-footer">Total Val: {curr_symbol}{total_inventory_val:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

if lead_time_shock > 0:
    st.warning(f"⚠️ **Disruption Simulation Active:** Lead times inflated by **+{lead_time_shock}%**. Notice the escalation in Reorder Points and High-Risk counts.")


# ======================================================================================
# 7. TABBED ENTERPRISE WORKFLOW
# ======================================================================================
tab_overview, tab_table, tab_sql, tab_abc, tab_po = st.tabs([
    "📊 Executive Analytics & Visualizations",
    "📋 Live Inventory & Procurement Table",
    "💾 SQL In-Memory Analytics Engine",
    "📐 ABC Pareto & EOQ Analysis",
    "🛒 Automated ERP Purchase Order Plan"
])

# --------------------------------------------------------------------------------------
# TAB 1: EXECUTIVE ANALYTICS & VISUALIZATIONS
# --------------------------------------------------------------------------------------
with tab_overview:
    st.markdown("#### 📈 Supply Chain Performance & Vulnerability Profiles")
    
    col_chart1, col_chart2 = st.columns([6, 4])
    
    with col_chart1:
        # Visual Component 1: Supplier Vulnerability Bar Breakdown
        supp_risk_df = filtered_df.groupby(["Supplier", "Stockout_Risk"]).size().reset_index(name="SKU_Count")
        fig_supp = px.bar(
            supp_risk_df,
            x="Supplier",
            y="SKU_Count",
            color="Stockout_Risk",
            barmode="group",
            title="<b>Supplier Risk Profile: Safe vs. High-Risk Inventory</b>",
            labels={"SKU_Count": "Number of SKUs", "Supplier": "Supplier Partner"},
            color_discrete_map={"High Risk": "#ef4444", "Safe": "#10b981"}
        )
        fig_supp.update_layout(
            margin=dict(l=10, r=10, t=50, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_supp, use_container_width=True)

    with col_chart2:
        # Visual Component 2: Stockout Risk Donut Chart
        risk_counts = filtered_df["Stockout_Risk"].value_counts().reset_index()
        risk_counts.columns = ["Stockout_Risk", "Count"]
        
        fig_donut = px.pie(
            risk_counts,
            names="Stockout_Risk",
            values="Count",
            hole=0.62,
            title="<b>Overall Inventory Health Distribution</b>",
            color="Stockout_Risk",
            color_discrete_map={"High Risk": "#ef4444", "Safe": "#10b981"}
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=2)))
        fig_donut.update_layout(
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            font=dict(family="Plus Jakarta Sans", size=12),
            annotations=[dict(text=f"<b>{total_skus}</b><br>SKUs", x=0.5, y=0.5, font_size=18, showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")
    
    col_chart3, col_chart4 = st.columns([5, 5])
    
    with col_chart3:
        # Visual Component 3: Current Stock vs. Reorder Point Scatter
        fig_scatter = px.scatter(
            filtered_df,
            x="Reorder_Point",
            y="Current_Stock",
            color="Stockout_Risk",
            hover_name="Part_Description",
            hover_data=["SKU_ID", "Supplier", "Category", "Daily_Demand", "Lead_Time_Days", "Safety_Stock"],
            title="<b>Inventory Health Boundary (Current Stock vs. Reorder Point)</b>",
            labels={"Reorder_Point": "Calculated Reorder Point (Units)", "Current_Stock": "Current Warehouse Stock (Units)"},
            color_discrete_map={"High Risk": "#ef4444", "Safe": "#10b981"},
            opacity=0.85
        )
        max_bound = max(filtered_df["Reorder_Point"].max(), filtered_df["Current_Stock"].max()) if len(filtered_df) > 0 else 1000
        fig_scatter.add_trace(
            go.Scatter(
                x=[0, max_bound],
                y=[0, max_bound],
                mode="lines",
                name="Safety Boundary (y = x)",
                line=dict(color="#64748b", dash="dash", width=2)
            )
        )
        fig_scatter.update_layout(
            margin=dict(l=10, r=10, t=50, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", size=12)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.caption("💡 *Points plotted below the dashed line operate below their Reorder Point threshold and require immediate replenishment.*")

    with col_chart4:
        # Visual Component 4: Category Risk Exposure
        cat_grp = filtered_df.groupby("Category").agg(
            Total=("SKU_ID", "count"),
            High_Risk=("Stockout_Risk", lambda x: (x == "High Risk").sum()),
            Avg_LT=("Lead_Time_Days", "mean")
        ).reset_index()
        cat_grp["Risk_Rate"] = (cat_grp["High_Risk"] / cat_grp["Total"] * 100).round(1)

        fig_cat = px.bar(
            cat_grp,
            x="Category",
            y="High_Risk",
            color="Risk_Rate",
            color_continuous_scale="Reds",
            title="<b>High-Risk Concentration Across Mechanical Categories</b>",
            labels={"High_Risk": "High-Risk SKU Count", "Risk_Rate": "Risk Rate (%)"},
            text="High_Risk"
        )
        fig_cat.update_traces(textposition='outside')
        fig_cat.update_layout(
            margin=dict(l=10, r=10, t=50, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", size=12)
        )
        st.plotly_chart(fig_cat, use_container_width=True)


# --------------------------------------------------------------------------------------
# TAB 2: LIVE INVENTORY TABLE & EXPORT
# --------------------------------------------------------------------------------------
with tab_table:
    st.markdown("#### 📋 Live Warehouse Procurement & Inventory Log")
    st.markdown("Real-time operational records with dynamic Reorder Points, safety buffers, stockout classifications, and runway days.")

    search_term = st.text_input("🔍 Quick Search by SKU ID, Component Name, or Category", placeholder="e.g. Hex Bolt, SKU-HYD-1025, Cylinder...")
    
    table_view = filtered_df.copy()
    if search_term:
        table_view = table_view[
            table_view["SKU_ID"].str.contains(search_term, case=False, na=False) |
            table_view["Part_Description"].str.contains(search_term, case=False, na=False) |
            table_view["Category"].str.contains(search_term, case=False, na=False)
        ]

    # Present polished Streamlit table using native modern column_config
    st.dataframe(
        table_view[[
            "SKU_ID", "Part_Description", "Category", "Supplier", "Lead_Time_Days",
            "Unit_Cost", "Daily_Demand", "Current_Stock", "Safety_Stock",
            "Reorder_Point", "Stockout_Risk", "Runway_Days", "Inventory_Value"
        ]],
        column_config={
            "SKU_ID": st.column_config.TextColumn("SKU ID", width="small"),
            "Part_Description": st.column_config.TextColumn("Component Specification", width="large"),
            "Category": st.column_config.TextColumn("Commodity", width="medium"),
            "Supplier": st.column_config.TextColumn("Vendor", width="small"),
            "Lead_Time_Days": st.column_config.NumberColumn("Lead Time", format="%d d"),
            "Unit_Cost": st.column_config.NumberColumn(f"Unit Cost ({curr_symbol})", format=f"{curr_symbol} %,.2f"),
            "Daily_Demand": st.column_config.NumberColumn("Daily Demand", format="%d u/d"),
            "Current_Stock": st.column_config.NumberColumn("Current Stock", format="%,d"),
            "Safety_Stock": st.column_config.NumberColumn("Safety Stock", format="%,d"),
            "Reorder_Point": st.column_config.NumberColumn("Reorder Point", format="%,d"),
            "Stockout_Risk": st.column_config.TextColumn("Risk Status", width="small"),
            "Runway_Days": st.column_config.NumberColumn("Runway", format="%.1f d"),
            "Inventory_Value": st.column_config.NumberColumn(f"Stock Valuation ({curr_symbol})", format=f"{curr_symbol} %,.2f")
        },
        use_container_width=True,
        height=480,
        hide_index=True
    )

    st.markdown("##### 📥 Data Export & ERP Synchronization")
    e_col1, e_col2 = st.columns(2)
    with e_col1:
        csv_filtered = table_view.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📄 Download Filtered Procurement Records ({len(table_view)} Rows)",
            data=csv_filtered,
            file_name="procurement_inventory_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )
    with e_col2:
        high_risk_csv = table_view[table_view["Stockout_Risk"] == "High Risk"].to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"🚨 Export High-Risk Critical Action List (CSV)",
            data=high_risk_csv,
            file_name="high_risk_urgent_procurement_action.csv",
            mime="text/csv",
            use_container_width=True
        )


# --------------------------------------------------------------------------------------
# TAB 3: SQL IN-MEMORY ANALYTICS ENGINE
# --------------------------------------------------------------------------------------
with tab_sql:
    st.markdown("#### 💾 In-Memory SQLite Analytics Engine & Multi-Tier Aggregations")
    st.markdown(
        "Demonstrating rigorous data engineering: All records are ingested into SQLite via SQLAlchemy with `StaticPool`. "
        "Analytical queries utilize conditional `CASE` statements and `GROUP BY` to isolate vendor risk and expedite capital."
    )

    # Advanced SQL Query 1: Supplier Performance & Capital Matrix
    supp_sql_query = f"""
    SELECT 
        Supplier,
        COUNT(SKU_ID) AS Total_SKUs,
        SUM(CASE WHEN Stockout_Risk = 'High Risk' THEN 1 ELSE 0 END) AS High_Risk_SKUs,
        SUM(CASE WHEN Stockout_Risk = 'Safe' THEN 1 ELSE 0 END) AS Safe_SKUs,
        ROUND(100.0 * SUM(CASE WHEN Stockout_Risk = 'High Risk' THEN 1 ELSE 0 END) / COUNT(SKU_ID), 1) AS Risk_Percentage,
        ROUND(AVG(Lead_Time_Days), 1) AS Avg_Lead_Time_Days,
        ROUND(AVG(Daily_Demand), 1) AS Avg_Daily_Demand,
        ROUND(SUM(Current_Stock * Unit_Cost), 2) AS Total_Valuation_{'INR' if is_inr else 'USD'},
        ROUND(SUM(CASE WHEN Stockout_Risk = 'High Risk' THEN (Reorder_Point - Current_Stock) * Unit_Cost ELSE 0 END), 2) AS Urgent_Procurement_Capital_{'INR' if is_inr else 'USD'}
    FROM procurement_inventory
    GROUP BY Supplier
    ORDER BY High_Risk_SKUs DESC, Risk_Percentage DESC;
    """
    
    supp_sql_res = run_sql_query(supp_sql_query, db_engine)

    st.markdown("##### 1. Supplier-Wise Risk Matrix & Expedite Budget (SQL `GROUP BY` + `CASE`)")
    st.dataframe(
        supp_sql_res,
        column_config={
            "Risk_Percentage": st.column_config.NumberColumn("Risk Exposure", format="%.1f%%"),
            "Avg_Lead_Time_Days": st.column_config.NumberColumn("Avg Lead Time", format="%.1f d"),
            f"Total_Valuation_{'INR' if is_inr else 'USD'}": st.column_config.NumberColumn(f"Inventory Valuation ({curr_symbol})", format=f"{curr_symbol} %,.2f"),
            f"Urgent_Procurement_Capital_{'INR' if is_inr else 'USD'}": st.column_config.NumberColumn(f"Urgent Expedite Capital ({curr_symbol})", format=f"{curr_symbol} %,.2f")
        },
        use_container_width=True,
        hide_index=True
    )

    with st.expander("🔍 View Executed SQL Query (Supplier Performance)"):
        st.code(supp_sql_query, language="sql")

    st.markdown("---")

    # Advanced SQL Query 2: Category Breakdown
    cat_sql_query = f"""
    SELECT 
        Category,
        COUNT(SKU_ID) AS Total_Items,
        SUM(CASE WHEN Stockout_Risk = 'High Risk' THEN 1 ELSE 0 END) AS High_Risk_Items,
        ROUND(100.0 * SUM(CASE WHEN Stockout_Risk = 'High Risk' THEN 1 ELSE 0 END) / COUNT(SKU_ID), 1) AS Category_Risk_Rate,
        ROUND(AVG(Lead_Time_Days), 1) AS Avg_Lead_Time,
        ROUND(SUM(Current_Stock * Unit_Cost), 2) AS Category_Inventory_Value
    FROM procurement_inventory
    GROUP BY Category
    ORDER BY High_Risk_Items DESC;
    """
    cat_sql_res = run_sql_query(cat_sql_query, db_engine)

    st.markdown("##### 2. Commodity Vulnerability Breakdown (SQL `GROUP BY` Aggregations)")
    st.dataframe(
        cat_sql_res,
        column_config={
            "Category_Risk_Rate": st.column_config.NumberColumn("Risk Rate", format="%.1f%%"),
            "Avg_Lead_Time": st.column_config.NumberColumn("Mean Lead Time", format="%.1f d"),
            "Category_Inventory_Value": st.column_config.NumberColumn(f"Inventory Value ({curr_symbol})", format=f"{curr_symbol} %,.2f")
        },
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # Live Interactive SQL Query Console
    st.markdown("##### 💻 Live Interactive SQL Query Console")
    st.markdown("Execute custom SQL queries against the active `procurement_inventory` table in the SQLite database:")

    default_custom_sql = f"""SELECT 
    SKU_ID, 
    Part_Description, 
    Supplier, 
    Lead_Time_Days, 
    Current_Stock, 
    Reorder_Point, 
    (Reorder_Point - Current_Stock) AS Deficit_Units,
    ROUND((Reorder_Point - Current_Stock) * Unit_Cost, 2) AS Expedite_Budget
FROM procurement_inventory
WHERE Stockout_Risk = 'High Risk'
ORDER BY Deficit_Units DESC
LIMIT 10;"""

    custom_sql = st.text_area("Enter Custom SQL Query:", value=default_custom_sql, height=130)
    
    if st.button("▶️ Execute Query", use_container_width=False):
        try:
            custom_res = run_sql_query(custom_sql, db_engine)
            st.success(f"✓ Query executed successfully. Returned {len(custom_res)} rows.")
            st.dataframe(custom_res, use_container_width=True)
        except Exception as e:
            st.error(f"❌ SQL Execution Error: {str(e)}")


# --------------------------------------------------------------------------------------
# TAB 4: ABC PARETO ANALYSIS & EOQ MODELING
# --------------------------------------------------------------------------------------
with tab_abc:
    st.markdown("#### 📐 Operations Research: ABC Pareto Classification & EOQ Modeling")
    st.markdown(
        "Industry-standard inventory prioritization: Items are categorized by annual financial consumption volume. "
        "Wilson's EOQ formula calculates the mathematically optimal purchase batch size to minimize total holding and ordering costs."
    )

    abc_summary = filtered_df.groupby("ABC_Class").agg(
        SKU_Count=("SKU_ID", "count"),
        High_Risk_Count=("Stockout_Risk", lambda x: (x == "High Risk").sum()),
        Total_Value=("Inventory_Value", "sum")
    ).reset_index()
    
    abc_summary["SKU_Share_Pct"] = (abc_summary["SKU_Count"] / abc_summary["SKU_Count"].sum() * 100).round(1)
    abc_summary["Value_Share_Pct"] = (abc_summary["Total_Value"] / abc_summary["Total_Value"].sum() * 100).round(1)

    abc_c1, abc_c2 = st.columns([5, 5])
    
    with abc_c1:
        st.markdown("##### ABC Inventory Pareto Summary")
        st.dataframe(
            abc_summary[[
                "ABC_Class", "SKU_Count", "SKU_Share_Pct", "High_Risk_Count", "Total_Value", "Value_Share_Pct"
            ]],
            column_config={
                "ABC_Class": st.column_config.TextColumn("Pareto Tier"),
                "SKU_Count": st.column_config.NumberColumn("SKU Count", format="%,d"),
                "SKU_Share_Pct": st.column_config.NumberColumn("SKU Share", format="%.1f%%"),
                "High_Risk_Count": st.column_config.NumberColumn("High Risk SKUs", format="%,d"),
                "Total_Value": st.column_config.NumberColumn(f"Total Valuation ({curr_symbol})", format=f"{curr_symbol} %,.2f"),
                "Value_Share_Pct": st.column_config.NumberColumn("Value Share", format="%.1f%%")
            },
            use_container_width=True,
            hide_index=True
        )

    with abc_c2:
        fig_abc = px.pie(
            abc_summary,
            names="ABC_Class",
            values="Total_Value",
            title="<b>Inventory Financial Value by ABC Tier</b>",
            color="ABC_Class",
            color_discrete_map={
                "Class A (High Value)": "#3b82f6",
                "Class B (Moderate)": "#8b5cf6",
                "Class C (Low Value)": "#94a3b8"
            }
        )
        fig_abc.update_traces(textposition='inside', textinfo='percent+label')
        fig_abc.update_layout(
            margin=dict(l=10, r=10, t=40, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            font=dict(family="Plus Jakarta Sans", size=12)
        )
        st.plotly_chart(fig_abc, use_container_width=True)

    st.markdown("---")
    st.markdown("##### 💡 Operations Research & Inventory Formulations:")
    st.latex(r"EOQ = \sqrt{\frac{2 \times D \times S}{H}} \quad \text{where } D = \text{Annual Demand}, \, S = \text{Order Cost}, \, H = 0.20 \times \text{Unit Cost}")
    st.latex(r"Reorder Point (ROP) = (L \times D) + SS = (\text{Lead Time Days} \times \text{Daily Demand}) + \text{Safety Stock}")


# --------------------------------------------------------------------------------------
# TAB 5: AUTOMATED PURCHASE ORDER (PO) GENERATOR
# --------------------------------------------------------------------------------------
with tab_po:
    st.markdown("#### 🛒 Automated Procurement Action Plan & Purchase Order Generator")
    st.markdown(
        "Prescriptive operations decision engine: Automatically groups urgent stockout items into vendor-specific purchase orders, "
        "calculates suggested order sizes using EOQ buffers, and exports clean batches ready for ERP upload (SAP/Oracle/Odoo)."
    )

    urgent_po_items = filtered_df[filtered_df["Stockout_Risk"] == "High Risk"].copy()
    
    if len(urgent_po_items) == 0:
        st.success("🎉 All inventory levels are healthy! Zero items currently require urgent purchase orders.")
    else:
        urgent_po_items["Total_PO_Cost"] = (urgent_po_items["Suggested_Order_Qty"] * urgent_po_items["Unit_Cost"]).round(2)
        
        po_kpi1, po_kpi2, po_kpi3 = st.columns(3)
        with po_kpi1:
            st.metric("Total Replenishment Orders", f"{len(urgent_po_items)} PO Lines")
        with po_kpi2:
            st.metric("Total Order Units", f"{urgent_po_items['Suggested_Order_Qty'].sum():,} Units")
        with po_kpi3:
            st.metric("Total Procurement Spend", f"{curr_symbol}{urgent_po_items['Total_PO_Cost'].sum():,.2f}")

        st.markdown("##### Recommended Urgent Purchase Orders (Sorted by Shortest Runway Days)")
        
        po_table = urgent_po_items[[
            "SKU_ID", "Part_Description", "Supplier", "Current_Stock", "Reorder_Point",
            "Runway_Days", "EOQ_Units", "Suggested_Order_Qty", "Unit_Cost", "Total_PO_Cost"
        ]].sort_values(by="Runway_Days", ascending=True)

        st.dataframe(
            po_table,
            column_config={
                "SKU_ID": st.column_config.TextColumn("SKU ID", width="small"),
                "Part_Description": st.column_config.TextColumn("Component Specification", width="large"),
                "Supplier": st.column_config.TextColumn("Vendor", width="small"),
                "Current_Stock": st.column_config.NumberColumn("Current Stock", format="%,d"),
                "Reorder_Point": st.column_config.NumberColumn("ROP", format="%,d"),
                "Runway_Days": st.column_config.NumberColumn("Runway", format="%.1f d"),
                "EOQ_Units": st.column_config.NumberColumn("EOQ Batch", format="%,d"),
                "Suggested_Order_Qty": st.column_config.NumberColumn("Recommended Order Qty", format="%,d"),
                "Unit_Cost": st.column_config.NumberColumn(f"Unit Cost ({curr_symbol})", format=f"{curr_symbol} %,.2f"),
                "Total_PO_Cost": st.column_config.NumberColumn(f"Estimated PO Spend ({curr_symbol})", format=f"{curr_symbol} %,.2f")
            },
            use_container_width=True,
            height=400,
            hide_index=True
        )

        po_export_csv = po_table.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Procurement PO Action Plan to ERP (CSV)",
            data=po_export_csv,
            file_name="urgent_procurement_purchase_orders.csv",
            mime="text/csv",
            use_container_width=True
        )

# ======================================================================================
# FOOTER
# ======================================================================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #94a3b8; font-size: 0.85rem; padding: 8px 0;">
        <b>ProcureOptix</b> | Inventory & Supply Chain Procurement Optimization Dashboard | 
        Enterprise Decision Support System | 
        Powered by Streamlit, SQLite, Pandas, NumPy & Plotly
    </div>
    """,
    unsafe_allow_html=True
)
