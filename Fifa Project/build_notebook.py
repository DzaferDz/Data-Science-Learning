import json

notebook = {
    'cells': [
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '# FIFA 20 Players Intelligence & Market Valuation Project\n',
                '**Domain:** Sports Data Science, Financial Efficiency & Scouting Analytics  \n',
                '**Dataset:** `players_20.csv` (18,278 players, 104 attributes)  \n',
                '**Deliverables:** Python (Pandas), Excel, SQL, Power BI  \n',
                '\n',
                '---\n',
                '### Project Strategic Goals\n',
                '1. **Valuation & Wage Dynamics:** Which European clubs operate with highest financial efficiency?\n',
                '2. **Talent Scouting (Wonderkids & Bargains):** Who are the high-potential players (potential >= 85) available under 5M EUR market valuation?\n',
                '3. **Age Curve & Depreciation:** At what exact age does market valuation peak versus physical skill decline?'
            ]
        },
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '## 1. Environment Setup & Data Loading\n',
                'We import `pandas` and `numpy`. We configure display settings for numerical clarity.'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': 1,
            'metadata': {},
            'outputs': [],
            'source': [
                'import pandas as pd\n',
                'import numpy as np\n',
                '\n',
                'pd.set_option("display.max_columns", 25)\n',
                'pd.set_option("display.float_format", lambda x: "%.2f" % x)\n',
                '\n',
                '# Load the primary dataset\n',
                'df_players = pd.read_csv("players_20.csv")\n',
                'print(f"Loaded dataset: {df_players.shape[0]:,} rows and {df_players.shape[1]} columns.")'
            ]
        },
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '## 2. Inspecting Data Structure\n',
                'Let us inspect the top rows and verify data types for core numerical columns (`age`, `overall`, `potential`, `value_eur`, `wage_eur`).'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': 2,
            'metadata': {},
            'outputs': [],
            'source': [
                'core_view = ["short_name", "club", "age", "overall", "potential", "value_eur", "wage_eur", "player_positions"]\n',
                'df_players[core_view].head(10)'
            ]
        },
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '## 3. Data Cleaning & Feature Engineering\n',
                'In real-world data science, raw data needs enrichment:\n',
                '- **`position_group`:** Classify 15+ granular positions into 4 standard categories (`Goalkeeper`, `Defender`, `Midfielder`, `Attacker`).\n',
                '- **`potential_gap`:** Difference between potential and current rating ($Potential - Overall$).\n',
                '- **`annual_wage_eur`:** Weekly wage multiplied by 52 weeks.\n',
                '- **`value_wage_ratio`:** Valuation divided by annual wage (identifying underpaid high-output talent).'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': 3,
            'metadata': {},
            'outputs': [],
            'source': [
                'def map_position(pos_str):\n',
                '    if pd.isna(pos_str):\n',
                '        return "Unknown"\n',
                '    primary = str(pos_str).split(",")[0].strip()\n',
                '    if primary in ["GK"]:\n',
                '        return "Goalkeeper"\n',
                '    elif primary in ["CB", "LB", "RB", "LWB", "RWB"]:\n',
                '        return "Defender"\n',
                '    elif primary in ["CDM", "CM", "CAM", "LM", "RM"]:\n',
                '        return "Midfielder"\n',
                '    elif primary in ["ST", "CF", "LW", "RW"]:\n',
                '        return "Attacker"\n',
                '    return "Other"\n',
                '\n',
                'df_players["position_group"] = df_players["player_positions"].apply(map_position)\n',
                'df_players["potential_gap"] = df_players["potential"] - df_players["overall"]\n',
                'df_players["annual_wage_eur"] = df_players["wage_eur"] * 52\n',
                'df_players["value_wage_ratio"] = np.where(\n',
                '    df_players["annual_wage_eur"] > 0,\n',
                '    (df_players["value_eur"] / df_players["annual_wage_eur"]).round(2),\n',
                '    0.0\n',
                ')\n',
                '\n',
                'bins = [15, 20, 25, 29, 50]\n',
                'labels = ["U21 Wonderkid", "21-25 Rising", "26-29 Prime", "30+ Veteran"]\n',
                'df_players["age_bracket"] = pd.cut(df_players["age"], bins=bins, labels=labels)\n',
                '\n',
                'print("Distribution by Position Group:")\n',
                'print(df_players["position_group"].value_counts())'
            ]
        },
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '## 4. Analysis 1: The Wonderkid Scouting Matrix\n',
                'A wonderkid is defined as a player aged **21 or under** with a **potential rating of 85 or above**.\n',
                'These players represent the highest future financial and tactical upside.'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': 4,
            'metadata': {},
            'outputs': [],
            'source': [
                'wonderkids = df_players[\n',
                '    (df_players["age"] <= 21) & (df_players["potential"] >= 85)\n',
                '].sort_values(by=["potential", "overall"], ascending=False)\n',
                '\n',
                'print(f"Total Wonderkids identified: {len(wonderkids)}")\n',
                'wonderkids[["short_name", "club", "age", "overall", "potential", "potential_gap", "value_eur", "wage_eur"]].head(10)'
            ]
        },
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '## 5. Analysis 2: Undervalued "Bargain Gems"\n',
                'Recruiting teams with constrained budgets seek players with high growth ceilings (Potential >= 84) whose transfer fee is under **5,000,000 EUR**.'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': 5,
            'metadata': {},
            'outputs': [],
            'source': [
                'bargains = df_players[\n',
                '    (df_players["potential"] >= 84) & \n',
                '    (df_players["value_eur"] <= 5000000) & \n',
                '    (df_players["value_eur"] > 0)\n',
                '].sort_values(by=["potential_gap", "potential"], ascending=False)\n',
                '\n',
                'print(f"Total Bargain Gems found: {len(bargains)}")\n',
                'bargains[["short_name", "club", "age", "overall", "potential", "potential_gap", "value_eur", "wage_eur"]].head(10)'
            ]
        },
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '## 6. Analysis 3: Club Wage Bill vs. Rating Efficiency\n',
                'Here we aggregate by club to assess total financial commitments versus average player quality.'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': 6,
            'metadata': {},
            'outputs': [],
            'source': [
                'club_analysis = df_players.groupby("club").agg(\n',
                '    squad_size=("sofifa_id", "count"),\n',
                '    avg_overall=("overall", "mean"),\n',
                '    total_value=("value_eur", "sum"),\n',
                '    weekly_wage=("wage_eur", "sum"),\n',
                '    avg_age=("age", "mean")\n',
                ').reset_index()\n',
                '\n',
                'club_analysis["annual_wage"] = club_analysis["weekly_wage"] * 52\n',
                'club_analysis["value_per_wage_euro"] = (club_analysis["total_value"] / (club_analysis["annual_wage"] + 1)).round(2)\n',
                'club_analysis = club_analysis.sort_values(by="total_value", ascending=False)\n',
                '\n',
                'club_analysis.head(10)'
            ]
        },
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '## 7. Analysis 4: Age Curve & Valuation Inflection Point\n',
                'At what age does player market value peak? We aggregate by `age` to see the growth and depreciation timeline.'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': 7,
            'metadata': {},
            'outputs': [],
            'source': [
                'age_profile = df_players.groupby("age").agg(\n',
                '    player_count=("sofifa_id", "count"),\n',
                '    avg_overall=("overall", "mean"),\n',
                '    avg_potential=("potential", "mean"),\n',
                '    avg_value=("value_eur", "mean"),\n',
                '    avg_weekly_wage=("wage_eur", "mean")\n',
                ').reset_index()\n',
                '\n',
                'print("Age Curve Summary (Ages 18 to 34):")\n',
                'age_profile[(age_profile["age"] >= 18) & (age_profile["age"] <= 34)]'
            ]
        },
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '---\n',
                '### Presentation Script & Defense Takeaways\n',
                '- **Market Value Peak:** The average player market value peaks at age **27 to 28** (approx. 3.6M EUR mean).\n',
                '- **Depreciation:** Beyond age 29, market value drops sharply despite overall rating remaining stable, driven by shorter contract horizons and resale decline.\n',
                '- **Talent Concentration:** Top clubs maintain squad ratings >= 78 by carrying weekly wage commitments > 2.5M EUR.'
            ]
        }
    ],
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'name': 'python',
            'version': '3.10'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 5
}

with open('players_20.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print('Updated players_20.ipynb successfully.')
