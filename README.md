# ProcureOptix

[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat&logo=python&logoColor=white)](https://python.org)
[![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An interactive supply chain procurement and inventory optimization platform. Built with Python, Streamlit, Plotly, and an in-memory SQLite relational database engine via SQLAlchemy.

---

## Overview

ProcureOptix provides operations and procurement teams with real-time visibility into warehouse stock levels, supplier lead-time variability, and stockout hazards. The system dynamically computes Reorder Points (ROP), calculates optimal batch sizes via Wilson's Economic Order Quantity (EOQ), performs Pareto ABC inventory classification, and generates structured purchase orders formatted for ERP ingestion.

---

## Key Capabilities

- **Dynamic Reorder Point (ROP) Calculation**: Automatically evaluates replenishment thresholds using supplier lead times, floor consumption rates, and statistical safety buffers:
  $$\text{ROP} = (\text{Lead Time Days} \times \text{Daily Demand}) + \text{Safety Stock}$$
- **Stockout Risk Identification**: Continuously flags critical deficits (`High Risk` vs. `Safe`) before inventory depletion impacts manufacturing operations.
- **Wilson's Economic Order Quantity (EOQ)**: Calculates cost-optimal purchase order batch sizes balancing ordering setup expenses against inventory holding costs:
  $$\text{EOQ} = \sqrt{\frac{2 \times D \times S}{H}}$$
- **Pareto ABC Inventory Classification**: Segment inventory into:
  - **Class A**: High-value items (top 70% of total annual consumption value)
  - **Class B**: Moderate-value items (next 20% of value)
  - **Class C**: Low-value bulk items (bottom 10% of value)
- **Relational In-Memory SQLite Engine**: Ingests procurement records into SQLite with persistent session connection pooling (`StaticPool`). Executes analytical queries utilizing `GROUP BY` and conditional `CASE` statements.
- **Interactive SQL Sandbox**: Embedded query console allowing execution of custom SQL statements against the active database schema in real time.
- **Supply Chain Shock Simulation**: Parameterized lead-time stress testing ($0\%\text{--}60\%$ surge) to assess buffer stock resilience against logistics delays and vendor bottlenecks.
- **Automated Purchase Order Export**: Aggregates urgent replenishment orders grouped by vendor with estimated spend, exportable to CSV for ERP systems (SAP, Oracle, Odoo).
- **Dual Currency Engine**: Seamlessly switch between **INR (₹)** and **USD ($)** with live price adjustments and formatted reporting.

---

## Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend & UI** | Streamlit, HTML5, Custom CSS |
| **Data Processing** | Pandas, NumPy |
| **Relational Database** | SQLite 3, SQLAlchemy (StaticPool) |
| **Data Visualization** | Plotly Express, Plotly Graph Objects |
| **Export Formats** | CSV (RFC 4180 compliant) |

---

## Repository Structure

```text
├── app.py              # Main application entry point & dashboard layout
├── requirements.txt    # Project dependencies
├── .gitignore          # Git exclusion rules
└── README.md           # Documentation
```

---

## Quickstart & Local Setup

### 1. Prerequisites
- Python 3.9 or higher
- Git

### 2. Clone Repository
```bash
git clone https://github.com/An32006shi/inventory-procurement-dashboard.git
cd inventory-procurement-dashboard
```

### 3. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Launch the Application
```bash
streamlit run app.py
```
The application will launch automatically at `http://localhost:8501`.

---

## Core SQL Queries

### Supplier Vulnerability & Expedite Capital
```sql
SELECT 
    Supplier,
    COUNT(SKU_ID) AS Total_SKUs,
    SUM(CASE WHEN Stockout_Risk = 'High Risk' THEN 1 ELSE 0 END) AS High_Risk_SKUs,
    SUM(CASE WHEN Stockout_Risk = 'Safe' THEN 1 ELSE 0 END) AS Safe_SKUs,
    ROUND(100.0 * SUM(CASE WHEN Stockout_Risk = 'High Risk' THEN 1 ELSE 0 END) / COUNT(SKU_ID), 1) AS Risk_Percentage,
    ROUND(AVG(Lead_Time_Days), 1) AS Avg_Lead_Time_Days,
    ROUND(AVG(Daily_Demand), 1) AS Avg_Daily_Demand,
    ROUND(SUM(Current_Stock * Unit_Cost), 2) AS Total_Valuation,
    ROUND(SUM(CASE WHEN Stockout_Risk = 'High Risk' THEN (Reorder_Point - Current_Stock) * Unit_Cost ELSE 0 END), 2) AS Urgent_Procurement_Capital
FROM procurement_inventory
GROUP BY Supplier
ORDER BY High_Risk_SKUs DESC, Risk_Percentage DESC;
```

---

## License

This project is licensed under the [MIT License](LICENSE).
