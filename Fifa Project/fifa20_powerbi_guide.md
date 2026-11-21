# FIFA 20 Power BI Architecture & Dashboard Blueprint

This blueprint outlines how to build an enterprise-grade scouting and squad valuation dashboard in Power BI using `fifa20_clean_scouting.csv`.

---

## 1. Data Model Architecture (Star Schema)

In production BI systems, we never rely on a single flat table for large reporting models. We normalize into a **Star Schema** with one central Fact table and surrounding Dimension tables:

```
          +-------------------+
          |     Dim_Clubs     |
          |  (club, league)   |
          +---------+---------+
                    | 1
                    |
                    | *
+-------------------+---+       * +----------------------+
|     Fact_Players      |<--------|    Dim_Nationality   |
| (sofifa_id, ratings,  |         |     (nationality)    |
|  wages, valuations)   |         +----------------------+
+---------+---------+---+
          | *       | *
          |         |
          | 1       | 1
+---------+---+   +-+--------------------+
| Dim_Position|   |   Dim_AgeBrackets    |
| (position)  |   |    (age_bracket)     |
+-------------+   +----------------------+
```

### Table Definitions:
1. **`Fact_Players`**: Central table containing grain-level player records (`sofifa_id`, `overall`, `potential`, `value_eur`, `wage_eur`, `pace`, `shooting`, etc.).
2. **`Dim_Clubs`**: Distinct clubs list. Connected to `Fact_Players[club]` (1-to-many, single cross-filter).
3. **`Dim_Nationality`**: Distinct nationality list. Connected to `Fact_Players[nationality]` (1-to-many).
4. **`Dim_Position`**: Distinct primary positions and position groups (`Goalkeeper`, `Defender`, `Midfielder`, `Attacker`).
5. **`Dim_AgeBrackets`**: Standardized age brackets (`U21 Wonderkid`, `21-25 Rising`, `26-29 Prime`, `30+ Veteran`).

---

## 2. Core DAX Measures Reference Table

Create a dedicated calculation group or measure table named `_Measures`:

### Measure 1: Total Squad Market Value
```dax
Total Market Value (€) = 
SUM(Fact_Players[value_eur])
```
*Format: Currency, display units in Millions (€0.00M).*

### Measure 2: Total Weekly Wage Commitment
```dax
Total Weekly Wage (€) = 
SUM(Fact_Players[wage_eur])
```
*Format: Currency, display units in Thousands (€0K).*

### Measure 3: Annualized Wage Bill
```dax
Annual Wage Bill (€) = 
[Total Weekly Wage (€)] * 52
```

### Measure 4: Squad Value-to-Wage Efficiency Ratio
Measures how many euros of player market asset value the club owns per single euro of annual wage paid.
```dax
Value to Wage Efficiency = 
DIVIDE([Total Market Value (€)], [Annual Wage Bill (€)], 0)
```

### Measure 5: Average Squad Rating
```dax
Average Rating = 
AVERAGE(Fact_Players[overall])
```

### Measure 6: Average Squad Potential
```dax
Average Potential = 
AVERAGE(Fact_Players[potential])
```

### Measure 7: Wonderkid Talent Count
Counts all high-upside youth assets under 22 years of age with a potential ceiling of 85+.
```dax
Wonderkid Count = 
CALCULATE(
    COUNTROWS(Fact_Players),
    Fact_Players[age] <= 21,
    Fact_Players[potential] >= 85
)
```

### Measure 8: Average Growth Gap
```dax
Average Growth Gap = 
AVERAGE(Fact_Players[potential_gap])
```

---

## 3. Two-Page Report Canvas Layout

### Page 1: Executive Squad Health & Financial Exposure
- **Top Metric Cards (KPI Band):**
  1. `[Total Market Value (€)]`
  2. `[Annual Wage Bill (€)]`
  3. `[Average Rating]`
  4. `[Wonderkid Count]`
- **Visual 1 (Scatter Plot):**
  - **X-Axis:** `[Total Weekly Wage (€)]`
  - **Y-Axis:** `[Average Rating]`
  - **Bubble Size:** `[Total Market Value (€)]`
  - **Details:** `club`
  - *Business Insight:* Clubs in the top-left quadrant are high-efficiency operators; clubs in the bottom-right are financially exposed.
- **Visual 2 (Bar Chart):** Top 10 Clubs by `[Total Market Value (€)]`.
- **Slicers:** `Dim_Clubs[club]`, `Dim_Nationality[nationality]`.

### Page 2: Talent Scouting & Recruitment Desk
- **Visual 1 (Scatter Plot - Age Curve):**
  - **X-Axis:** `age`
  - **Y-Axis:** `[Average Rating]` and `[Average Potential]`
  - *Scouting Insight:* Displays the convergence point where potential and overall ratings meet (age 27-28).
- **Visual 2 (Matrix / Table):** Filterable Scouting Table
  - Columns: `Player Name`, `Club`, `Position`, `Age`, `Overall`, `Potential`, `Value (€)`, `Weekly Wage (€)`, `Efficiency Multiple`.
  - Conditional Formatting: Green data bars on `Potential`, heatmap background on `Value to Wage Efficiency`.
- **Interactive Slicers:**
  - `Dim_Position[position_group]` (Single-select buttons: All / Forward / Midfield / Defense / GK).
  - `Fact_Players[age]` (Slider: 16 to 40).
  - `Fact_Players[value_eur]` (Slider: €0 to €105M).
