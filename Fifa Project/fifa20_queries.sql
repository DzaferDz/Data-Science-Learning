-- =====================================================================
-- FIFA 20 SCOUTING & FINANCIAL EFFICIENCY INTELLIGENCE
-- Dataset: players_20 (18,278 records)
-- Purpose: Practical SQL queries for player valuation, scouting,
--          and wage optimization analytics.
-- =====================================================================

-- ---------------------------------------------------------------------
-- QUERY 1: The Top Wonderkids Under 21
-- Identifies top young talents with potential >= 88, ordered by upside.
-- ---------------------------------------------------------------------
SELECT 
    short_name,
    club,
    nationality,
    age,
    overall,
    potential,
    (potential - overall) AS potential_gap,
    value_eur,
    wage_eur
FROM players_20
WHERE age <= 21 AND potential >= 88
ORDER BY potential DESC, overall DESC;

-- ---------------------------------------------------------------------
-- QUERY 2: Club Financial Efficiency (Market Value vs. Wage Spend)
-- Aggregates squad size, total valuation, and weekly wage bill.
-- Calculates the efficiency ratio (Value per annual wage euro).
-- ---------------------------------------------------------------------
SELECT 
    club,
    COUNT(sofifa_id) AS squad_size,
    ROUND(AVG(overall), 1) AS avg_squad_rating,
    ROUND(AVG(age), 1) AS avg_age,
    SUM(value_eur) AS total_market_value_eur,
    SUM(wage_eur) AS weekly_wage_bill_eur,
    SUM(wage_eur) * 52 AS annual_wage_bill_eur,
    ROUND(CAST(SUM(value_eur) AS FLOAT) / (SUM(wage_eur) * 52 + 1), 2) AS value_to_wage_ratio
FROM players_20
WHERE club IS NOT NULL AND club != ''
GROUP BY club
HAVING COUNT(sofifa_id) >= 20
ORDER BY total_market_value_eur DESC
LIMIT 15;

-- ---------------------------------------------------------------------
-- QUERY 3: Undervalued "Bargain Gems"
-- Players with potential >= 85 and market value <= €5,000,000.
-- Perfect for recruitment teams operating under tight capital limits.
-- ---------------------------------------------------------------------
SELECT 
    short_name,
    club,
    nationality,
    player_positions,
    age,
    overall,
    potential,
    (potential - overall) AS potential_gap,
    value_eur,
    wage_eur
FROM players_20
WHERE potential >= 85 
  AND value_eur <= 5000000 
  AND value_eur > 0
ORDER BY potential_gap DESC, potential DESC
LIMIT 20;

-- ---------------------------------------------------------------------
-- QUERY 4: Window Function - Top Rated Player per Nation
-- Uses DENSE_RANK() to find the #1 player representing each country.
-- ---------------------------------------------------------------------
WITH RankedPlayers AS (
    SELECT 
        short_name,
        nationality,
        club,
        overall,
        potential,
        value_eur,
        DENSE_RANK() OVER (PARTITION BY nationality ORDER BY overall DESC, value_eur DESC) as nat_rank
    FROM players_20
)
SELECT 
    nationality,
    short_name,
    club,
    overall,
    potential,
    value_eur
FROM RankedPlayers
WHERE nat_rank = 1
ORDER BY overall DESC
LIMIT 25;

-- ---------------------------------------------------------------------
-- QUERY 5: Contract Expiry Risk (Expiring within 12 Months)
-- Identifies high-quality assets (Overall >= 82) whose contract ends in 2020.
-- High leverage for free transfers or cut-price negotiations.
-- ---------------------------------------------------------------------
SELECT 
    short_name,
    club,
    nationality,
    age,
    overall,
    value_eur,
    wage_eur,
    contract_valid_until
FROM players_20
WHERE contract_valid_until IN ('2020', '2020.0')
  AND overall >= 82
ORDER BY value_eur DESC;

-- ---------------------------------------------------------------------
-- QUERY 6: CTE Analysis - Overpaid Clubs vs. Market Benchmark
-- Compares club wage averages against global league averages.
-- ---------------------------------------------------------------------
WITH GlobalStats AS (
    SELECT 
        AVG(wage_eur) AS global_avg_wage,
        AVG(overall) AS global_avg_overall
    FROM players_20
    WHERE wage_eur > 0
),
ClubStats AS (
    SELECT 
        club,
        COUNT(sofifa_id) AS squad_size,
        AVG(wage_eur) AS club_avg_wage,
        AVG(overall) AS club_avg_overall
    FROM players_20
    WHERE club IS NOT NULL
    GROUP BY club
    HAVING COUNT(sofifa_id) >= 20
)
SELECT 
    c.club,
    c.squad_size,
    ROUND(c.club_avg_wage, 0) AS club_avg_weekly_wage,
    ROUND(c.club_avg_overall, 1) AS club_avg_rating,
    ROUND(c.club_avg_wage - g.global_avg_wage, 0) AS wage_premium_above_global,
    ROUND(c.club_avg_overall - g.global_avg_overall, 1) AS rating_premium_above_global
FROM ClubStats c
CROSS JOIN GlobalStats g
ORDER BY wage_premium_above_global DESC
LIMIT 15;
