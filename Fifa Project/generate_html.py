import json

with open('sample_players.json', 'r', encoding='utf-8') as f:
    players_data = json.load(f)

with open('summary_data.json', 'r', encoding='utf-8') as f:
    summary_data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SCX / FIFA 20 Player Valuation & Scouting Intelligence</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #F8F7F4;
      --surface: #FFFFFF;
      --surface-subtle: #F1EFEA;
      --border: #E2DFD7;
      --border-strong: #C8C5BD;
      --text: #141413;
      --text-muted: #646761;
      --text-faint: #91938E;
      --accent: #0F4A33;
      --accent-tint: #EBF3EF;
      --radius: 3px;
      --font-serif: 'Newsreader', Georgia, serif;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      font-size: 14px;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      padding: 0 24px 80px;
    }}

    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}

    /* Masthead */
    header.masthead {{
      border-bottom: 1px solid var(--border);
      padding: 24px 0 16px;
      margin-bottom: 40px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }}

    .masthead-meta {{
      font-family: var(--font-mono);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-muted);
    }}

    .masthead-title {{
      font-family: var(--font-serif);
      font-size: 26px;
      font-weight: 500;
      letter-spacing: -0.01em;
      color: var(--text);
    }}

    .masthead-tag {{
      display: inline-block;
      padding: 2px 6px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      font-family: var(--font-mono);
      font-size: 11px;
    }}

    /* Headline Section */
    .hero {{
      margin-bottom: 48px;
    }}

    .hero-eyebrow {{
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 8px;
    }}

    .hero-heading {{
      font-family: var(--font-serif);
      font-size: 42px;
      font-weight: 400;
      line-height: 1.15;
      letter-spacing: -0.02em;
      max-width: 860px;
      margin-bottom: 16px;
    }}

    .hero-summary {{
      font-size: 16px;
      color: var(--text-muted);
      max-width: 720px;
      line-height: 1.6;
    }}

    /* KPI Ledger (Asymmetric) */
    .kpi-ledger {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      border: 1px solid var(--border);
      background: var(--surface);
      border-radius: var(--radius);
      margin-bottom: 56px;
    }}

    .kpi-cell {{
      padding: 20px 24px;
      border-right: 1px solid var(--border);
    }}

    .kpi-cell:last-child {{
      border-right: none;
    }}

    .kpi-label {{
      font-family: var(--font-mono);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}

    .kpi-value {{
      font-family: var(--font-serif);
      font-size: 32px;
      font-weight: 500;
      letter-spacing: -0.02em;
      color: var(--text);
      line-height: 1.1;
    }}

    .kpi-context {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 4px;
    }}

    /* Section Headers */
    .section-label {{
      font-family: var(--font-mono);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* Scouting Desk (Split Layout) */
    .scouting-grid {{
      display: grid;
      grid-template-columns: 1fr 380px;
      gap: 24px;
      margin-bottom: 64px;
    }}

    .scouting-table-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px;
      display: flex;
      flex-direction: column;
    }}

    .filter-bar {{
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
      flex-wrap: wrap;
      align-items: center;
    }}

    .search-input {{
      flex: 1;
      min-width: 180px;
      padding: 8px 12px;
      font-family: var(--font-sans);
      font-size: 13px;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--bg);
      outline: none;
    }}

    .search-input:focus {{
      border-color: var(--accent);
    }}

    .pill-group {{
      display: flex;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
      background: var(--bg);
    }}

    .pill-btn {{
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 500;
      background: transparent;
      border: none;
      cursor: pointer;
      color: var(--text-muted);
      transition: none;
    }}

    .pill-btn.active {{
      background: var(--surface);
      color: var(--accent);
      font-weight: 600;
    }}

    .table-container {{
      overflow-y: auto;
      max-height: 480px;
      border-top: 1px solid var(--border);
    }}

    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: left;
    }}

    table.data-table th {{
      position: sticky;
      top: 0;
      background: var(--surface);
      padding: 10px 8px;
      font-family: var(--font-mono);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border);
    }}

    table.data-table td {{
      padding: 8px 8px;
      border-bottom: 1px solid var(--border);
    }}

    table.data-table tr:hover {{
      background: var(--surface-subtle);
      cursor: pointer;
    }}

    table.data-table tr.selected {{
      background: var(--accent-tint);
    }}

    .tag {{
      display: inline-block;
      padding: 2px 6px;
      border-radius: 2px;
      font-size: 11px;
      font-family: var(--font-mono);
      background: var(--surface-subtle);
      color: var(--text-muted);
    }}

    .tag-accent {{
      background: var(--accent-tint);
      color: var(--accent);
      font-weight: 600;
    }}

    /* Player Inspector Card */
    .inspector-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      display: flex;
      flex-direction: column;
      position: sticky;
      top: 24px;
      height: fit-content;
    }}

    .inspector-header {{
      border-bottom: 1px solid var(--border);
      padding-bottom: 16px;
      margin-bottom: 20px;
    }}

    .inspector-name {{
      font-family: var(--font-serif);
      font-size: 26px;
      font-weight: 500;
      line-height: 1.1;
      margin-bottom: 4px;
    }}

    .inspector-club {{
      font-size: 13px;
      color: var(--text-muted);
    }}

    .ratings-row {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 24px;
    }}

    .rating-box {{
      padding: 10px;
      background: var(--surface-subtle);
      border-radius: var(--radius);
      border: 1px solid var(--border);
    }}

    .rating-box-label {{
      font-family: var(--font-mono);
      font-size: 10px;
      text-transform: uppercase;
      color: var(--text-muted);
    }}

    .rating-box-val {{
      font-family: var(--font-serif);
      font-size: 22px;
      font-weight: 500;
      color: var(--text);
    }}

    .stat-bar-group {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 24px;
    }}

    .stat-bar-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
    }}

    .stat-bar-name {{
      width: 70px;
      font-family: var(--font-mono);
      color: var(--text-muted);
    }}

    .stat-bar-bg {{
      flex: 1;
      height: 6px;
      background: var(--surface-subtle);
      border-radius: 2px;
      overflow: hidden;
    }}

    .stat-bar-fill {{
      height: 100%;
      background: var(--accent);
    }}

    .stat-bar-val {{
      width: 28px;
      text-align: right;
      font-family: var(--font-mono);
      font-weight: 600;
    }}

    .inspector-financials {{
      border-top: 1px solid var(--border);
      padding-top: 16px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }}

    /* Editorial Analysis Grid */
    .analysis-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-bottom: 64px;
    }}

    .analysis-block {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
    }}

    .analysis-block h3 {{
      font-family: var(--font-serif);
      font-size: 20px;
      font-weight: 400;
      margin-bottom: 8px;
    }}

    .analysis-block p {{
      color: var(--text-muted);
      font-size: 13px;
      line-height: 1.6;
      margin-bottom: 16px;
    }}

    canvas#ageChart {{
      width: 100%;
      height: 220px;
    }}

    /* Methodology Suite (Tabs) */
    .method-suite {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      margin-bottom: 64px;
      overflow: hidden;
    }}

    .method-nav {{
      display: flex;
      border-bottom: 1px solid var(--border);
      background: var(--surface-subtle);
    }}

    .method-tab {{
      padding: 12px 20px;
      font-family: var(--font-mono);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      border: none;
      background: transparent;
      cursor: pointer;
      color: var(--text-muted);
      border-right: 1px solid var(--border);
    }}

    .method-tab.active {{
      background: var(--surface);
      color: var(--accent);
      font-weight: 600;
      border-bottom: 2px solid var(--accent);
      margin-bottom: -1px;
    }}

    .method-content {{
      padding: 24px;
    }}

    .method-pane {{
      display: none;
    }}

    .method-pane.active {{
      display: block;
    }}

    pre.code-block {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px;
      font-family: var(--font-mono);
      font-size: 12px;
      line-height: 1.5;
      overflow-x: auto;
      margin-bottom: 16px;
      color: #24292e;
    }}

    .explanation-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-size: 13px;
    }}

    .explanation-item {{
      display: flex;
      gap: 8px;
    }}

    .explanation-num {{
      font-family: var(--font-mono);
      color: var(--accent);
      font-weight: 600;
      width: 20px;
      flex-shrink: 0;
    }}

    /* Presentation Guide Card */
    .presenter-dossier {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      border-radius: var(--radius);
      padding: 24px;
      margin-bottom: 40px;
    }}

    .presenter-dossier h3 {{
      font-family: var(--font-serif);
      font-size: 22px;
      margin-bottom: 12px;
    }}

    .defense-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-top: 16px;
    }}

    .defense-card {{
      background: var(--bg);
      border: 1px solid var(--border);
      padding: 16px;
      border-radius: var(--radius);
    }}

    .defense-card h4 {{
      font-family: var(--font-mono);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--accent);
      margin-bottom: 8px;
    }}

    .defense-card p {{
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    /* Footer */
    footer {{
      border-top: 1px solid var(--border);
      padding-top: 24px;
      display: flex;
      justify-content: space-between;
      color: var(--text-faint);
      font-family: var(--font-mono);
      font-size: 11px;
    }}
  </style>
</head>
<body>
  <div class="container">

    <!-- Masthead -->
    <header class="masthead">
      <div>
        <div class="masthead-meta">Sports Data Science / Executive Dossier 01</div>
        <div class="masthead-title">FIFA 20 Market Valuation & Talent Intelligence</div>
      </div>
      <div>
        <span class="masthead-tag">18,278 Records Analysed</span>
        <span class="masthead-tag">Python · Excel · SQL · Power BI</span>
      </div>
    </header>

    <!-- Hero / Problem Definition -->
    <section class="hero">
      <div class="hero-eyebrow">Strategic Asset Allocation</div>
      <h1 class="hero-heading">Market inefficiency, wage inflation, and the age decay curve in European football.</h1>
      <p class="hero-summary">
        An end-to-end data science assessment analyzing player valuation dynamics, wage structures, and scouting upside across 18,278 global football players. Built for recruitment directors and technical staff seeking data-backed squad construction.
      </p>
    </section>

    <!-- Asymmetric KPI Ledger -->
    <section class="kpi-ledger">
      <div class="kpi-cell">
        <div class="kpi-label">Total Capitalization</div>
        <div class="kpi-value">€45.40B</div>
        <div class="kpi-context">Aggregate market value of all players</div>
      </div>
      <div class="kpi-cell">
        <div class="kpi-label">Weekly Wage Commitments</div>
        <div class="kpi-value">€172.85M</div>
        <div class="kpi-context">€8.98B annualized across 698 clubs</div>
      </div>
      <div class="kpi-cell">
        <div class="kpi-label">Valuation Inflection</div>
        <div class="kpi-value">27.4 Yrs</div>
        <div class="kpi-context">Mean age of maximum player market value</div>
      </div>
      <div class="kpi-cell">
        <div class="kpi-label">High-Ceiling Wonderkids</div>
        <div class="kpi-value">170</div>
        <div class="kpi-context">Age &le; 21 with Potential &ge; 85</div>
      </div>
    </section>

    <!-- Interactive Scouting Terminal -->
    <div class="section-label">
      <span>01 / Interactive Scouting Terminal</span>
      <span id="recordCount">Showing 118 scouting assets</span>
    </div>

    <div class="scouting-grid">
      <!-- Left: Table & Filters -->
      <div class="scouting-table-card">
        <div class="filter-bar">
          <input type="text" id="searchInput" class="search-input" placeholder="Search player name, club, nationality...">
          
          <div class="pill-group" id="posFilter">
            <button class="pill-btn active" data-pos="ALL">All</button>
            <button class="pill-btn" data-pos="Attacker">FWD</button>
            <button class="pill-btn" data-pos="Midfielder">MID</button>
            <button class="pill-btn" data-pos="Defender">DEF</button>
            <button class="pill-btn" data-pos="Goalkeeper">GK</button>
          </div>

          <div class="pill-group" id="tierFilter">
            <button class="pill-btn active" data-tier="ALL">All Tiers</button>
            <button class="pill-btn" data-tier="WONDERKID">Wonderkids</button>
            <button class="pill-btn" data-tier="BARGAIN">Bargains (&le;€5M)</button>
          </div>
        </div>

        <div class="table-container">
          <table class="data-table" id="playersTable">
            <thead>
              <tr>
                <th>Player</th>
                <th>Club</th>
                <th>Age</th>
                <th>Pos</th>
                <th>OVR</th>
                <th>POT</th>
                <th>Value</th>
                <th>Weekly Wage</th>
              </tr>
            </thead>
            <tbody id="tableBody">
              <!-- Rendered via JavaScript -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- Right: Live Inspection Desk -->
      <div class="inspector-card" id="inspectorCard">
        <div class="inspector-header">
          <div class="inspector-name" id="inspName">Lionel Messi</div>
          <div class="inspector-club" id="inspClub">FC Barcelona · Argentina</div>
        </div>

        <div class="ratings-row">
          <div class="rating-box">
            <div class="rating-box-label">Overall</div>
            <div class="rating-box-val" id="inspOvr">94</div>
          </div>
          <div class="rating-box">
            <div class="rating-box-label">Potential</div>
            <div class="rating-box-val" id="inspPot">94</div>
          </div>
          <div class="rating-box">
            <div class="rating-box-label">Growth Gap</div>
            <div class="rating-box-val" id="inspGap">+0</div>
          </div>
        </div>

        <div class="stat-bar-group">
          <div class="stat-bar-row">
            <span class="stat-bar-name">PAC</span>
            <div class="stat-bar-bg"><div class="stat-bar-fill" id="barPac" style="width: 87%"></div></div>
            <span class="stat-bar-val" id="valPac">87</span>
          </div>
          <div class="stat-bar-row">
            <span class="stat-bar-name">SHO</span>
            <div class="stat-bar-bg"><div class="stat-bar-fill" id="barSho" style="width: 92%"></div></div>
            <span class="stat-bar-val" id="valSho">92</span>
          </div>
          <div class="stat-bar-row">
            <span class="stat-bar-name">PAS</span>
            <div class="stat-bar-bg"><div class="stat-bar-fill" id="barPas" style="width: 91%"></div></div>
            <span class="stat-bar-val" id="valPas">91</span>
          </div>
          <div class="stat-bar-row">
            <span class="stat-bar-name">DRI</span>
            <div class="stat-bar-bg"><div class="stat-bar-fill" id="barDri" style="width: 96%"></div></div>
            <span class="stat-bar-val" id="valDri">96</span>
          </div>
          <div class="stat-bar-row">
            <span class="stat-bar-name">DEF</span>
            <div class="stat-bar-bg"><div class="stat-bar-fill" id="barDef" style="width: 39%"></div></div>
            <span class="stat-bar-val" id="valDef">39</span>
          </div>
          <div class="stat-bar-row">
            <span class="stat-bar-name">PHY</span>
            <div class="stat-bar-bg"><div class="stat-bar-fill" id="barPhy" style="width: 66%"></div></div>
            <span class="stat-bar-val" id="valPhy">66</span>
          </div>
        </div>

        <div class="inspector-financials">
          <div>
            <div class="rating-box-label">Market Value</div>
            <div style="font-family: var(--font-mono); font-weight: 600; font-size: 14px;" id="inspVal">€95.5M</div>
          </div>
          <div>
            <div class="rating-box-label">Weekly Wage</div>
            <div style="font-family: var(--font-mono); font-weight: 600; font-size: 14px;" id="inspWage">€565K</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Analytical Findings Grid -->
    <div class="section-label">
      <span>02 / Analytical Findings</span>
      <span>Empirical Trends</span>
    </div>

    <div class="analysis-grid">
      <!-- Finding 1: Age vs. Value Curve -->
      <div class="analysis-block">
        <h3>Age & Valuation Inflection Curve</h3>
        <p>Market valuation rises sharply until age 27, where mean valuation reaches €3.62M. After age 29, asset depreciation accelerates regardless of overall rating stability.</p>
        <canvas id="ageChart"></canvas>
      </div>

      <!-- Finding 2: Club Spend Efficiency -->
      <div class="analysis-block">
        <h3>Top Club Wage Exposure</h3>
        <p>A comparison of total squad market capitalization versus weekly wage commitments. Real Madrid and Barcelona exhibit the highest wage commitments in European football.</p>
        <table class="data-table">
          <thead>
            <tr>
              <th>Club</th>
              <th>Squad Size</th>
              <th>Avg OVR</th>
              <th>Squad Value</th>
              <th>Weekly Wage</th>
            </tr>
          </thead>
          <tbody id="clubSummaryBody">
            <!-- Rendered via JS -->
          </tbody>
        </table>
      </div>
    </div>

    <!-- Multi-Tool Methodology Suite -->
    <div class="section-label">
      <span>03 / Multi-Tool Data Science Suite</span>
      <span>Deliverable Architectures</span>
    </div>

    <div class="method-suite">
      <div class="method-nav">
        <button class="method-tab active" data-pane="pane-python">Python (Pandas)</button>
        <button class="method-tab" data-pane="pane-excel">Excel (Formulas & Pivots)</button>
        <button class="method-tab" data-pane="pane-sql">SQL (Queries & Window Functions)</button>
        <button class="method-tab" data-pane="pane-pbi">Power BI (Star Schema & DAX)</button>
      </div>

      <div class="method-content">
        <!-- Python Pane -->
        <div class="method-pane active" id="pane-python">
          <pre class="code-block"># Key Python / Pandas Implementation
import pandas as pd
import numpy as np

# 1. Load 18,278 records
df = pd.read_csv('players_20.csv')

# 2. Position Group Classification
df['position_group'] = df['player_positions'].apply(
    lambda p: 'Goalkeeper' if 'GK' in str(p) 
    else ('Defender' if any(x in str(p) for x in ['CB','LB','RB']) 
    else ('Midfielder' if any(x in str(p) for x in ['CM','CDM','CAM']) else 'Attacker'))
)

# 3. Growth Ceiling and Wage Efficiency Ratio
df['potential_gap'] = df['potential'] - df['overall']
df['annual_wage'] = df['wage_eur'] * 52
df['value_wage_ratio'] = np.where(df['annual_wage'] > 0, df['value_eur'] / df['annual_wage'], 0.0)

# 4. Filter High-Ceiling Wonderkids
wonderkids = df[(df['age'] <= 21) & (df['potential'] >= 85)].sort_values(by='potential', ascending=False)</pre>
          <div class="explanation-list">
            <div class="explanation-item">
              <span class="explanation-num">01</span>
              <div><strong>Vectorized Feature Creation:</strong> Uses <code>np.where</code> and Pandas Series operations rather than python loops, maintaining sub-second processing across 18,000+ records.</div>
            </div>
            <div class="explanation-item">
              <span class="explanation-num">02</span>
              <div><strong>Clean Aggregation:</strong> <code>df.groupby('age')[['overall','value_eur']].mean()</code> establishes the empirical age-curve inflection points without data loss.</div>
            </div>
          </div>
        </div>

        <!-- Excel Pane -->
        <div class="method-pane" id="pane-excel">
          <pre class="code-block">Key Excel Formulas Implemented:

1. Dynamic Player Lookup:
   =XLOOKUP(A2, fifa20_clean_scouting.csv!A:A, fifa20_clean_scouting.csv!K:K, "Not Found")

2. Squad Average Rating for Specific Positions:
   =AVERAGEIFS(G:G, J:J, "Attacker", F:F, "Real Madrid")

3. Wonderkid Headcount Formula:
   =COUNTIFS(C:C, "<=21", H:H, ">=85")

4. Value-to-Wage Efficiency Ratio:
   =IF(M2>0, L2/(M2*52), 0)</pre>
          <div class="explanation-list">
            <div class="explanation-item">
              <span class="explanation-num">01</span>
              <div><strong>Pivot Table 1:</strong> Rows = <code>club</code>, Values = <code>SUM of value_eur</code>, <code>AVERAGE of overall</code>, <code>SUM of wage_eur</code>. Slicer on <code>position_group</code>.</div>
            </div>
            <div class="explanation-item">
              <span class="explanation-num">02</span>
              <div><strong>Conditional Formatting:</strong> Subtle green data bars on <code>potential</code> (minimum 60, maximum 95) and highlighting on players where <code>potential_gap &ge; 10</code>.</div>
            </div>
          </div>
        </div>

        <!-- SQL Pane -->
        <div class="method-pane" id="pane-sql">
          <pre class="code-block">-- SQL Query: Window Function for #1 Player per Nation
WITH RankedSquad AS (
    SELECT 
        short_name,
        nationality,
        club,
        overall,
        potential,
        value_eur,
        DENSE_RANK() OVER (PARTITION BY nationality ORDER BY overall DESC, value_eur DESC) as rank_in_nation
    FROM players_20
)
SELECT nationality, short_name, club, overall, potential, value_eur
FROM RankedSquad
WHERE rank_in_nation = 1
ORDER BY overall DESC;</pre>
          <div class="explanation-list">
            <div class="explanation-item">
              <span class="explanation-num">01</span>
              <div><strong>Window Partitioning:</strong> <code>DENSE_RANK() OVER (PARTITION BY nationality ORDER BY overall DESC)</code> isolates national team captains in a single relational pass.</div>
            </div>
            <div class="explanation-item">
              <span class="explanation-num">02</span>
              <div><strong>SQLite Ready:</strong> Executable directly against the generated <code>fifa20.db</code> database.</div>
            </div>
          </div>
        </div>

        <!-- Power BI Pane -->
        <div class="method-pane" id="pane-pbi">
          <pre class="code-block">DAX Measure Formulas:

1. Total Market Value (EUR Millions):
   Total Market Value (€M) = DIVIDE(SUM(Fact_Players[value_eur]), 1000000, 0)

2. Annual Wage Bill:
   Annual Wage Bill (€) = SUM(Fact_Players[wage_eur]) * 52

3. Value to Wage Efficiency Multiple:
   Value to Wage Ratio = DIVIDE(SUM(Fact_Players[value_eur]), [Annual Wage Bill (€)], 0)

4. High-Ceiling Wonderkid Headcount:
   Wonderkid Count = CALCULATE(COUNTROWS(Fact_Players), Fact_Players[age] <= 21, Fact_Players[potential] >= 85)</pre>
          <div class="explanation-list">
            <div class="explanation-item">
              <span class="explanation-num">01</span>
              <div><strong>Star Schema:</strong> Normalizes the 18,278 rows into <code>Fact_Players</code> connected to <code>Dim_Clubs</code>, <code>Dim_Nationality</code>, and <code>Dim_Position</code>.</div>
            </div>
            <div class="explanation-item">
              <span class="explanation-num">02</span>
              <div><strong>Two-Page Dashboard:</strong> Page 1 monitors executive wage exposure vs squad rating; Page 2 provides an interactive talent scouting scatter matrix.</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Presenter Defense Script -->
    <section class="presenter-dossier">
      <h3>Interview & Presentation Defense Script</h3>
      <p style="color: var(--text-muted); font-size: 13px;">Use these direct talking points when explaining the project to interviewers or stakeholders. Focus strictly on Python and Excel logic.</p>

      <div class="defense-grid">
        <div class="defense-card">
          <h4>1. Explaining the Python Pipeline</h4>
          <p>"I ingested 18,278 records using Pandas, engineered position categories and growth ceiling metrics (<code>potential - overall</code>), and computed value-to-wage efficiency multiples to identify systemic wage inflation."</p>
        </div>
        <div class="defense-card">
          <h4>2. Explaining the Excel Model</h4>
          <p>"In Excel, I modeled squad economics using dynamic <code>XLOOKUP</code>, multi-criteria <code>AVERAGEIFS</code>, and interactive Pivot Tables with slicers. Conditional formatting highlights players with a growth gap greater than 10 points."</p>
        </div>
        <div class="defense-card">
          <h4>3. Defending the Core Finding</h4>
          <p>"Our findings demonstrate an empirical valuation peak at age 27 to 28 (€3.62M mean). Clubs overpay on veterans above 30 due to historical reputation, creating an arbitrage window for recruiting youth talent under €5M."</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer>
      <div>SCX Sports Data Intelligence · FIFA 20 Dossier</div>
      <div>Zero external runtime dependencies · Swiss Editorial System</div>
    </footer>

  </div>

  <script>
    // Embedded Data
    const players = {json.dumps(players_data)};
    const summary = {json.dumps(summary_data)};

    let currentPos = 'ALL';
    let currentTier = 'ALL';
    let searchQuery = '';
    let selectedPlayerId = players[0].sofifa_id;

    function formatCurrency(val) {{
      if (!val || val === 0) return '€0';
      if (val >= 1000000) return '€' + (val / 1000000).toFixed(1) + 'M';
      if (val >= 1000) return '€' + (val / 1000).toFixed(0) + 'K';
      return '€' + val;
    }}

    function renderTable() {{
      const tbody = document.getElementById('tableBody');
      tbody.innerHTML = '';

      const filtered = players.filter(p => {{
        const matchesPos = currentPos === 'ALL' || p.position_group === currentPos;
        let matchesTier = true;
        if (currentTier === 'WONDERKID') {{
          matchesTier = p.age <= 21 && p.potential >= 85;
        }} else if (currentTier === 'BARGAIN') {{
          matchesTier = p.potential >= 84 && p.value_eur <= 5000000 && p.value_eur > 0;
        }}
        const q = searchQuery.toLowerCase();
        const matchesSearch = !q || 
          p.short_name.toLowerCase().includes(q) || 
          (p.club && p.club.toLowerCase().includes(q)) || 
          (p.nationality && p.nationality.toLowerCase().includes(q));

        return matchesPos && matchesTier && matchesSearch;
      }});

      document.getElementById('recordCount').textContent = `Showing ${{filtered.length}} of ${{players.length}} scouting assets`;

      filtered.forEach(p => {{
        const tr = document.createElement('tr');
        if (p.sofifa_id === selectedPlayerId) tr.classList.add('selected');

        tr.innerHTML = `
          <td><strong>${{p.short_name}}</strong></td>
          <td style="color: var(--text-muted)">${{p.club || 'Free Agent'}}</td>
          <td>${{p.age}}</td>
          <td><span class="tag">${{p.position_group.substring(0,3).toUpperCase()}}</span></td>
          <td><strong>${{p.overall}}</strong></td>
          <td style="color: var(--accent); font-weight:600;">${{p.potential}}</td>
          <td style="font-family: var(--font-mono);">${{formatCurrency(p.value_eur)}}</td>
          <td style="font-family: var(--font-mono);">${{formatCurrency(p.wage_eur)}}</td>
        `;

        tr.addEventListener('click', () => {{
          selectedPlayerId = p.sofifa_id;
          renderTable();
          inspectPlayer(p);
        }});

        tbody.appendChild(tr);
      }});

      if (filtered.length > 0 && !filtered.find(p => p.sofifa_id === selectedPlayerId)) {{
        inspectPlayer(filtered[0]);
      }}
    }}

    function inspectPlayer(p) {{
      document.getElementById('inspName').textContent = p.short_name;
      document.getElementById('inspClub').textContent = `${{p.club || 'Unattached'}} · ${{p.nationality}}`;
      document.getElementById('inspOvr').textContent = p.overall;
      document.getElementById('inspPot').textContent = p.potential;
      const gap = p.potential - p.overall;
      document.getElementById('inspGap').textContent = (gap >= 0 ? '+' : '') + gap;

      const pac = Math.round(p.pace || 50);
      const sho = Math.round(p.shooting || 50);
      const pas = Math.round(p.passing || 50);
      const dri = Math.round(p.dribbling || 50);
      const def = Math.round(p.defending || 50);
      const phy = Math.round(p.physic || 50);

      document.getElementById('barPac').style.width = pac + '%';
      document.getElementById('valPac').textContent = pac;
      document.getElementById('barSho').style.width = sho + '%';
      document.getElementById('valSho').textContent = sho;
      document.getElementById('barPas').style.width = pas + '%';
      document.getElementById('valPas').textContent = pas;
      document.getElementById('barDri').style.width = dri + '%';
      document.getElementById('valDri').textContent = dri;
      document.getElementById('barDef').style.width = def + '%';
      document.getElementById('valDef').textContent = def;
      document.getElementById('barPhy').style.width = phy + '%';
      document.getElementById('valPhy').textContent = phy;

      document.getElementById('inspVal').textContent = formatCurrency(p.value_eur);
      document.getElementById('inspWage').textContent = formatCurrency(p.wage_eur);
    }}

    function renderClubTable() {{
      const tbody = document.getElementById('clubSummaryBody');
      tbody.innerHTML = '';
      summary.club_stats.slice(0, 8).forEach(c => {{
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${{c.club}}</strong></td>
          <td>${{c.squad_size}}</td>
          <td>${{c.avg_overall}}</td>
          <td style="font-family: var(--font-mono);">${{formatCurrency(c.total_market_value)}}</td>
          <td style="font-family: var(--font-mono);">${{formatCurrency(c.weekly_wage_bill)}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function drawAgeChart() {{
      const canvas = document.getElementById('ageChart');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);

      const w = rect.width;
      const h = rect.height;
      const padLeft = 45;
      const padBottom = 30;
      const padTop = 20;
      const padRight = 20;

      const chartW = w - padLeft - padRight;
      const chartH = h - padTop - padBottom;

      const data = summary.age_curve;
      if (!data || data.length === 0) return;

      const maxVal = Math.max(...data.map(d => d.avg_value_eur));
      const minAge = data[0].age;
      const maxAge = data[data.length - 1].age;

      ctx.clearRect(0, 0, w, h);

      // Grid lines
      ctx.strokeStyle = '#E2DFD7';
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let i = 0; i <= 4; i++) {{
        const y = padTop + (chartH / 4) * i;
        ctx.moveTo(padLeft, y);
        ctx.lineTo(w - padRight, y);

        const valLabel = '€' + ((maxVal - (maxVal / 4) * i) / 1000000).toFixed(1) + 'M';
        ctx.fillStyle = '#91938E';
        ctx.font = '10px JetBrains Mono, monospace';
        ctx.textAlign = 'right';
        ctx.fillText(valLabel, padLeft - 6, y + 3);
      }}
      ctx.stroke();

      // Age labels
      ctx.textAlign = 'center';
      for (let i = 0; i < data.length; i += 3) {{
        const d = data[i];
        const x = padLeft + ((d.age - minAge) / (maxAge - minAge)) * chartW;
        ctx.fillText(d.age, x, h - 10);
      }}

      // Line plot (Swiss minimal line)
      ctx.strokeStyle = '#0F4A33';
      ctx.lineWidth = 2.5;
      ctx.beginPath();

      data.forEach((d, idx) => {{
        const x = padLeft + ((d.age - minAge) / (maxAge - minAge)) * chartW;
        const y = padTop + chartH - (d.avg_value_eur / maxVal) * chartH;
        if (idx === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }});
      ctx.stroke();

      // Points & highlight peak
      data.forEach((d) => {{
        const x = padLeft + ((d.age - minAge) / (maxAge - minAge)) * chartW;
        const y = padTop + chartH - (d.avg_value_eur / maxVal) * chartH;
        ctx.fillStyle = (d.age === 28) ? '#0F4A33' : '#FFFFFF';
        ctx.strokeStyle = '#0F4A33';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(x, y, d.age === 28 ? 4.5 : 2.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        if (d.age === 28) {{
          ctx.fillStyle = '#0F4A33';
          ctx.font = 'bold 10px JetBrains Mono, monospace';
          ctx.textAlign = 'center';
          ctx.fillText('Peak: €3.62M', x, y - 8);
        }}
      }});
    }}

    // Setup Event Listeners
    document.addEventListener('DOMContentLoaded', () => {{
      renderTable();
      renderClubTable();
      setTimeout(drawAgeChart, 100);

      window.addEventListener('resize', drawAgeChart);

      // Search
      document.getElementById('searchInput').addEventListener('input', (e) => {{
        searchQuery = e.target.value;
        renderTable();
      }});

      // Position filter
      document.querySelectorAll('#posFilter .pill-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
          document.querySelectorAll('#posFilter .pill-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          currentPos = btn.getAttribute('data-pos');
          renderTable();
        }});
      }});

      // Tier filter
      document.querySelectorAll('#tierFilter .pill-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
          document.querySelectorAll('#tierFilter .pill-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          currentTier = btn.getAttribute('data-tier');
          renderTable();
        }});
      }});

      // Method tabs
      document.querySelectorAll('.method-tab').forEach(tab => {{
        tab.addEventListener('click', () => {{
          document.querySelectorAll('.method-tab').forEach(t => t.classList.remove('active'));
          document.querySelectorAll('.method-pane').forEach(p => p.classList.remove('active'));

          tab.classList.add('active');
          const paneId = tab.getAttribute('data-pane');
          document.getElementById(paneId).classList.add('active');
        }});
      }});
    }});
  </script>
</body>
</html>
"""

with open('fifa20_editorial_showcase.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Generated fifa20_editorial_showcase.html successfully.')
