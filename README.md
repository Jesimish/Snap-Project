# Snap-Project

This repository was created to publicly showcase my Python data engineering code. Because the raw data source files are too large to host directly within GitHub's file limits, they have been omitted from this repository. 

* Please see [Resources.md](Resources.md) for direct links to the raw data sources.
* Please see [Process_and_Methodology.md](Process_and_Methodology.md) for a detailed walkthrough of the project lifecycle, business logic, and analytical decisions.

---

# SNAP Efficacy & Food Access Dashboard

An end-to-end data engineering and visualization project analyzing the relationships between Supplemental Nutrition Assistance Program (SNAP) utilization, median household income gaps, and geographical food retail networks across the United States.

## Project Overview
This project began with a curiosity about how effectively SNAP benefits support households across different regions. While initially aiming for high-density, localized monthly analysis, data privacy constraints and decentralized reporting required a strategic pivot. 

By scaling up to structured annual metrics, this project successfully bridges **US Census demographic data**, **USDA Food and Nutrition Service (FNS) retailer databases**, and **Bureau of Economic Analysis (BEA) Regional Price Parity data** into a unified, high-performance interactive dashboard.

### Core Architecture
1. **Data Cleaning & Automation (Python / Pandas):** Automating the extraction, cleaning, and un-pivoting ("melting") of complex, nested federal data structures.
2. **Data Modeling & Consolidation (SQL / DBeaver):** Combining distinct regional datasets into a single source of truth while applying pre-calculated statistical aggregations to optimize dashboard load times.
3. **Interactive Analysis (Tableau):** Building user-facing visualizations that capture systemic trends—such as the geographic accessibility of retailers versus actual consumer spending power.

---

## Key Analytical Insights

### 1. The Convenience vs. Cost Structural Gap
A deep-dive into the USDA food firm redemption data reveals a striking structural inefficiency regarding physical food access:
* **Convenience Stores** account for roughly **44.3%** of all authorized SNAP retailers nationwide.
* Despite their massive geographic footprint, they capture only **5.2%** of total benefit redemptions.
* Conversely, **Supermarkets and Superstores** account for only ~**15.1%** of authorized locations but capture a massive **82.5%** of total benefit redemptions.

This highlights an critical economic behavior: SNAP participants heavily prioritize high-volume, lower-cost grocery infrastructure over immediate local convenience, highlighting the impact of "food deserts" where supermarkets are missing.

### 2. Data Governance & Economic Normalization
To prevent misrepresenting household spending power, two major rules were enforced in the SQL layer:
* **Purchasing Power Correction:** Nominal benefit amounts were adjusted using Regional Price Parity (RPP) to accurately evaluate the real-world value of a dollar from state to state.
* **Pre-Aggregation Over Averages:** Monthly enrollment tracking was aggregate-modeled in SQL first. This bypassed a common visualization issue where BI tools incorrectly calculate sums of pre-calculated monthly averages.

---

## Technical Implementation Details

### Python ETL Pipeline
Federal datasets (specifically US Census Tables like `B22008` and `S2201`) frequently output as wide-format pivot tables cluttered with demographic noise and complex, multi-tiered headers (e.g., `State!!Households receiving food stamps!!Estimate`). 

The Python script included in this repository handles:
* Iterative folder scanning to dynamically ingest multi-year CSV sheets.
* Target row filtering to strip away unneeded demographic subsets.
* **Data Melting:** Converting wide columns into long-format relational database rows.
* **Regex Header Mapping:** Truncating multi-line strings into standardized state identifiers and FIPS-compatible codes.

### Database Optimization (SQL)
Rather than executing resource-heavy multi-table joins inside Tableau at runtime, all relational modeling was pre-compiled using SQL within **DBeaver**. 
* Merged un-pivoted demographic tables with spatial retailer counts.
* Standardized geographic keys across distinct datasets to ensure clean, zero-loss joins.
* **Performance Impact:** Drastically decreased metadata payload sizes, ensuring fluid rendering and high shareability on Tableau Public.

---

## Dashboard Technical Fixes

During the development of the Tableau visualization layer, specific table calculation anomalies were resolved to ensure data integrity:
* **Top 5 / Bottom 5 Component Scope:** Fixed an issue where context filters or table directions (`Table down` vs. `Table across`) caused calculation thresholds to mismatch. Solved by explicitly fixing the calculation scope directly to the geographical dimension.
* **Donut Chart Percentage Labels:** Fixed a calculation error where standard `TOTAL()` summaries evaluated chart slices independently (returning a rank or calculation value of `1` for every slice). Addressed by mapping the explicit table calculation to compute along the precise dimension slicing the visualization.
