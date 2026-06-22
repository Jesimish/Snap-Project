# Data Resources & Links

This file contains the data directory and direct download references for all the public federal datasets utilized in the **SNAP Efficacy and Food Access Dashboard** pipeline. 

Because the raw data source files exceed GitHub's hosting file limits, they are omitted from the repository. Use the links below to gather the raw matrices for replication.

---

## 1. United States Census Bureau
Demographic benchmarks, population densities, and household tracking are derived from the **American Community Survey (ACS) 1-Year and 5-Year Estimates Detailed Tables**.

* **Table B22008: Median Household Income Gaps**
    * **Description:** Captures the median household income in the past 12 months (in inflation-adjusted dollars) broken down specifically by households receiving Food Stamps/SNAP versus households not receiving benefits. 
    * **Utilization:** Used for the pipeline's Python extraction script to measure regional financial gaps without demographic or multi-tier table noise.
    * **Source Link:** [US Census Bureau - Table B22008](https://data.census.gov/table/ACSDT1Y2023.B22008)
* **Table S2201: SNAP Characteristics**
    * **Description:** A broader thematic subject table mapping the macro socio-economic conditions of SNAP households (poverty tracking, work status, and household size distribution).
    * **Source Link:** [US Census Bureau - Table S2201](https://data.census.gov/table/ACSST5Y2023.S2201)

## 2. United States Department of Agriculture (USDA)
Retail infrastructure, geographic boundaries of authorization, and real-world benefit allocation totals are derived from the **Food and Nutrition Service (FNS)** and **Economic Research Service (ERS)**.

* **FNS SNAP Retailer Database (Food Firm Data)**
    * **Description:** Complete registry of all authorized SNAP-accepting retailers nationwide. Used to group firm classifications (Supermarkets, Convenience Stores, Box Stores) and map spatial access density points against localized household cohorts.
    * **Source Link:** [USDA FNS Food Resource Data](https://www.ers.usda.gov/topics/food-nutrition-assistance/supplemental-nutrition-assistance-program-snap/key-statistics-and-research)
* **Characteristics of SNAP Households & Quality Control Databases**
    * **Description:** Annual administrative microdata and sample files breaking down national and state-level gross/net incomes, benefit utilization distributions, and aggregate annual outlays.
    * **Source Link:** [USDA SNAP Quality Control Data Portal](https://snapqcdata.net/datafiles)

## 3. Bureau of Economic Analysis (BEA)
* **Regional Price Parities (RPP) by State and Metro Area**
    * **Description:** Measures the differences in price levels for goods and services across states and metropolitan areas relative to the national average.
    * **Utilization:** Imported into DBeaver during the SQL data-modeling stage to normalize nominal monthly SNAP allocations into localized purchasing power valuations.
    * **Source Link:** [BEA Interactive Data Tables - Regional Income](https://www.bea.gov/data/prices-inflation/regional-price-parities)
