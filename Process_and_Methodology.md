# Process & Methodology: SNAP Efficacy Project

This document outlines the end-to-end engineering lifecycle, data transformations, business logic adjustments, and visualization methodology behind the **SNAP Efficacy and Food Access Dashboard**.

---

## 1. Initial Curiosity & Project Pivot

### The Original Vision
The project began with a core question: *How effectively do local regions support vulnerable populations via the Supplemental Nutrition Assistance Program (SNAP)?* The initial objective was to construct a highly granular, county-and-ZIP-level monthly dashboard. The intention was to map local "outreach impact" by cross-referencing:
* Monthly enrollment metrics.
* Local public learning/advertising materials regarding SNAP benefits.
* Hyper-local tracking of what item types benefits were spent on.

### The Real-World Data Constraint (The Pivot)
Upon checking public administrative records, strict data privacy walls (specifically designed to protect participant anonymity) and highly decentralized county reporting made this granular scope impossible. Publicly available SNAP data is structurally constrained as follows:
1. **No Local Purchase Itemization:** Transaction-level details ("what SNAP is actually spent on") are protected at the individual user level and are not public.
2. **Decentralized Local Reporting:** Educational outreach and marketing methods are managed locally by county offices and are not aggregated into structured public data.
3. **Sample Size Limitations:** Highly detailed demographic tracking (like the USDA Quality Control databases) relies on household sampling, restricting the statistics strictly to state and national macro levels rather than county-by-county cells.

### The Strategic Solution
To build a functional, reliable analytics piece without compromising data truth, the project scope was broadened and simplified. Rather than looking at monthly micro-movements, the architecture pivoted to an annual, state-and-county aggregate analysis. By substituting localized text data with **USDA Food Firm spatial registries** and **US Census income gap matrices**, the objective successfully shifted to exploring the intersection of **regional financial stability** and **physical retailer density**.

---

## 2. Data Gathering & Engineering Pipeline

The data journey progressed through three main stages: extraction, modeling, and business logic engineering.

### Step 1: Python ETL & Multi-Year Automation
Federal data exports from the US Census Bureau (Tables `B22008` and `S2201`) typically generate wide-format pivot tables with nested headers (e.g., `State!!Households receiving food stamps!!Estimate`). These structures require flattening before they can be ingested into databases. 

A custom Python pipeline using the `pandas` library was built to automate the following actions:
* **Directory Scanning:** Looping dynamically through multi-year CSV sheets to build historical depth.
* **Row Extraction & Filtering:** Target row filtering to isolate specific rows containing the median income differences between SNAP-receiving and non-SNAP-receiving households, stripping away unneeded demographic subsets.
* **Data Melting:** Reshaping wide columns into long relational rows (stacking geographic observations into a single normalized column).
* **Regex Header Cleaning:** Processing multi-line database strings into clean, standardized state names and FIPS-compatible keys.

### Step 2: Relational Modeling in SQL (DBeaver)
To optimize dashboard performance and facilitate easier distribution on Tableau Public, all heavy computation was shifted away from Tableau's live rendering engine. Relational modeling was handled directly in **DBeaver** using SQL to build a pre-compiled source table:
* **Geographic Alignment:** Standardizing geographical keys across distinct Census and USDA datasets to ensure clean, zero-loss outer and inner joins.
* **Spatial Pre-compilation:** Aggregating thousands of raw USDA retailer points into county-level summaries (calculating total authorized retail locations by firm type per geographic area) before connecting to the BI tool.

### Step 3: Business Logic & Normalization
To ensure accurate economic comparisons, specific parameters were enforced during database modeling:
* **Purchasing Power Correction:** Nominal SNAP allocations were adjusted utilizing Regional Price Parity (RPP) index factors from the Bureau of Economic Analysis (BEA). This normalized values to reflect the real-world utility of a benefit dollar across different state economies.
* **Data Governance Against Flawed Averages:** In order to track benefit trends accurately without distorting numbers, enrollment volumes were aggregate-modeled in SQL first. This bypassed the typical business intelligence pitfall where dashboards incorrectly calculate sums of pre-calculated monthly averages.

---

## 3. Data Visualization & Dashboard Engineering

The visualization phase translated the modeled data layers into an interactive map environment, requiring specific technical overrides to maintain analytical accuracy.

### Resolution of Tableau Order of Operations & Scope Anomalies

#### 1. Top 5 / Bottom 5 Component Scope Fix
* **The Problem:** The "Bottom 5 Counties" visualization initially returned values higher than those listed in the "Top 5" component. This occurred because the underlying `RANK()` table calculation defaults to standard `Table (across)` or `Table (down)` directions, ranking data partitions based on visual placement rather than factual value.
* **The Fix:** The table calculation's execution direction was overridden, explicitly setting the calculation to compute along the precise geographic dimensions. This forced the calculation engine to accurately rank counties against one another regardless of how they were filtered on the dashboard.

#### 2. Donut Chart Percentage Label Aggregation Fix
* **The Problem:** A donut chart showing retailer distribution types initially evaluated every independent slice at a uniform valuation of `1` (or displaying identical baseline percentages like `5.9%`). This happened because the `TOTAL()` calculation summary function was executing in isolation for each slice rather than scanning the total pie space.
* **The Fix:** The Table Calculation scope was remapped to explicitly compute along the firm category dimension slicing the chart. This restored proper denominator evaluation, allowing percentages to compute accurately relative to the total sum of all categories combined.

---

## 4. Key Findings & Strategic Takeaways

* **Retail Inefficiencies:** The data reveals that while Convenience Stores make up **44.34%** of authorized SNAP retail environments, they receive only **5.19%** of actual benefit redemptions. Supermarkets and Superstores capture the overwhelming majority (**82.58%**) of redemptions despite making up only **15.14%** of authorized locations. This underscores an economic reality: SNAP users actively travel past immediate, local convenience entries to spend benefits at high-volume grocery setups where real-world purchasing power is optimized.
* **Architecture Impact:** Pre-compiling data aggregates within the SQL database layer reduced metadata payload sizes significantly. This optimization ensures fluid geo-spatial map rendering and low processing latency for end-users on Tableau Public.
