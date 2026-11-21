"""
FIFA 20 Complete Data Science Pipeline
Dataset: players_20.csv (18,278 players, 104 attributes)
Focus: Data cleaning, exploratory data analysis, wage efficiency metrics,
       wonderkid scouting, and presentation dataset exports.
"""

import pandas as pd
import numpy as np

def run_fifa_analysis():
    print("=" * 60)
    print("STEP 1: LOADING & INSPECTING DATASET")
    print("=" * 60)
    
    # 1. Load CSV
    df = pd.read_csv('players_20.csv')
    print(f"Total rows (players): {df.shape[0]:,}")
    print(f"Total columns (attributes): {df.shape[1]}")
    
    # 2. Position group classification
    def categorize_position(pos):
        if pd.isna(pos):
            return "Unknown"
        primary = str(pos).split(',')[0].strip()
        if primary in ['GK']:
            return "Goalkeeper"
        elif primary in ['CB', 'LB', 'RB', 'LWB', 'RWB']:
            return "Defender"
        elif primary in ['CDM', 'CM', 'CAM', 'LM', 'RM']:
            return "Midfielder"
        elif primary in ['ST', 'CF', 'LW', 'RW']:
            return "Attacker"
        return "Other"

    df['position_group'] = df['player_positions'].apply(categorize_position)
    
    # 3. Feature engineering
    df['potential_gap'] = df['potential'] - df['overall']
    df['annual_wage_eur'] = df['wage_eur'] * 52
    
    # Value efficiency ratio: market value created per euro of annual wage
    # (High ratio = club gets massive value relative to wage paid)
    df['value_wage_ratio'] = np.where(
        df['annual_wage_eur'] > 0,
        (df['value_eur'] / df['annual_wage_eur']).round(2),
        0.0
    )
    
    # Age brackets
    bins = [15, 20, 25, 29, 50]
    labels = ['U21 Wonderkid', '21-25 Rising', '26-29 Prime', '30+ Veteran']
    df['age_bracket'] = pd.cut(df['age'], bins=bins, labels=labels)
    
    print("\nPlayer distribution by position group:")
    print(df['position_group'].value_counts())
    
    print("\nPlayer distribution by age bracket:")
    print(df['age_bracket'].value_counts())
    
    print("\n" + "=" * 60)
    print("STEP 2: SCOUTING INTELLIGENCE EXPORTS")
    print("=" * 60)
    
    # Core columns for clean reporting
    core_cols = [
        'sofifa_id', 'short_name', 'long_name', 'age', 'age_bracket',
        'nationality', 'club', 'overall', 'potential', 'potential_gap',
        'position_group', 'player_positions', 'value_eur', 'wage_eur',
        'annual_wage_eur', 'value_wage_ratio', 'pace', 'shooting',
        'passing', 'dribbling', 'defending', 'physic', 'preferred_foot'
    ]
    clean_df = df[core_cols].copy()
    
    # Export 1: Cleaned Master Scouting Sheet (CSV)
    clean_df.to_csv('fifa20_clean_scouting.csv', index=False)
    print("✓ Created: fifa20_clean_scouting.csv (18,278 records)")
    
    # Export 2: Top Wonderkids (Age <= 21, Potential >= 85)
    wonderkids = clean_df[
        (clean_df['age'] <= 21) & (clean_df['potential'] >= 85)
    ].sort_values(by=['potential', 'overall'], ascending=False)
    wonderkids.to_csv('fifa20_top_wonderkids.csv', index=False)
    print(f"✓ Created: fifa20_top_wonderkids.csv ({len(wonderkids)} players)")
    
    # Export 3: Bargain Gems (Potential >= 84, Value <= €5,000,000)
    bargains = clean_df[
        (clean_df['potential'] >= 84) & 
        (clean_df['value_eur'] <= 5000000) & 
        (clean_df['value_eur'] > 0)
    ].sort_values(by=['potential_gap', 'potential'], ascending=False)
    bargains.to_csv('fifa20_bargain_gems.csv', index=False)
    print(f"✓ Created: fifa20_bargain_gems.csv ({len(bargains)} players)")
    
    # Export 4: Club Financial & Rating Efficiency
    club_stats = clean_df.groupby('club').agg(
        squad_size=('sofifa_id', 'count'),
        avg_overall=('overall', 'mean'),
        avg_potential=('potential', 'mean'),
        total_market_value=('value_eur', 'sum'),
        weekly_wage_bill=('wage_eur', 'sum'),
        avg_age=('age', 'mean')
    ).reset_index()
    club_stats['annual_wage_bill'] = club_stats['weekly_wage_bill'] * 52
    club_stats['value_to_wage_multiple'] = (
        club_stats['total_market_value'] / (club_stats['annual_wage_bill'] + 1)
    ).round(2)
    club_stats['avg_overall'] = club_stats['avg_overall'].round(1)
    club_stats['avg_potential'] = club_stats['avg_potential'].round(1)
    club_stats['avg_age'] = club_stats['avg_age'].round(1)
    
    club_stats_sorted = club_stats.sort_values(by='total_market_value', ascending=False)
    club_stats_sorted.to_csv('fifa20_club_efficiency.csv', index=False)
    print(f"✓ Created: fifa20_club_efficiency.csv ({len(club_stats_sorted)} clubs)")
    
    # Export 5: Age Trajectory
    age_curve = clean_df.groupby('age').agg(
        player_count=('sofifa_id', 'count'),
        avg_overall=('overall', 'mean'),
        avg_potential=('potential', 'mean'),
        avg_value_eur=('value_eur', 'mean'),
        avg_wage_eur=('wage_eur', 'mean')
    ).reset_index().round(1)
    age_curve.to_csv('fifa20_age_trajectory.csv', index=False)
    print(f"✓ Created: fifa20_age_trajectory.csv ({len(age_curve)} age points)")
    
    print("\n" + "=" * 60)
    print("STEP 3: KEY STATISTICAL INSIGHTS FOR PRESENTATION")
    print("=" * 60)
    print(f"1. Total Market Valuation: €{clean_df['value_eur'].sum():,.0f}")
    print(f"2. Total Weekly Wage Bill: €{clean_df['wage_eur'].sum():,.0f}")
    print(f"3. Overall Rating Peak Age: {age_curve.loc[age_curve['avg_overall'].idxmax()]['age']:.0f} years old (avg {age_curve['avg_overall'].max():.1f})")
    print(f"4. Market Value Peak Age: {age_curve.loc[age_curve['avg_value_eur'].idxmax()]['age']:.0f} years old (avg €{age_curve['avg_value_eur'].max():,.0f})")
    print("5. Top 3 Clubs by Total Squad Value:")
    for _, row in club_stats_sorted.head(3).iterrows():
        print(f"   - {row['club']}: €{row['total_market_value']:,.0f} (Avg Rating: {row['avg_overall']}, Weekly Wage: €{row['weekly_wage_bill']:,.0f})")

if __name__ == "__main__":
    run_fifa_analysis()
