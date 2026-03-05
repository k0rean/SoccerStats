"""Data loading and caching for SoccerStats."""
import os
import streamlit as st
import pandas as pd
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "soccerstats"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# League codes with flags (from feature/streamlit-dashboard)
LEAGUE_URLS = {
    "🇬🇧 Premier League": "E0",
    "🇪🇸 La Liga": "SP1",
    "🇩🇪 Bundesliga": "D1",
    "🇮🇹 Serie A": "I1",
    "🇫🇷 Ligue 1": "F1",
    "🇵🇹 Liga Portugal": "P1",
    "🇳🇱 Eredivisie": "N1",
    "🇧🇪 Belgian Pro": "B1",
    "🇹🇷 Super Lig": "T1",
    "🇬🇷 Super League Greece": "G1",
    "🇸🇦 Saudi Pro": "SAU",
    "🇦🇪 UAE League": "UAE",
    "🇦🇷 Argentina Liga": "ARG",
    "🇧🇷 Brasileiro": "BRA",
}

CURRENT_SEASON = "2025/2026"


def get_cache_path(league: str, season: str) -> Path:
    """Get cache file path for a league/season."""
    filename = f"{league}_{season.replace('/', '-')}.csv"
    return CACHE_DIR / filename


@st.cache_data(ttl=3600)
def load_match_data(league: str, season: str) -> pd.DataFrame:
    """
    Load match data for a league and season.
    Cached for 1 hour to avoid repeated downloads.
    """
    cache_file = get_cache_path(league, season)
    
    if cache_file.exists():
        try:
            df = pd.read_csv(cache_file)
            if not df.empty:
                return df
        except Exception:
            pass  # Fall through to download
    
    # Download from football-data.co.uk
    url = _build_url(league, season)
    if not url:
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(url)
        # Cache the data
        df.to_csv(cache_file, index=False)
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()


def _build_url(league: str, season: str) -> str | None:
    """Build the URL for downloading data."""
    league_code = LEAGUE_URLS.get(league)
    if not league_code:
        return None
    
    # Convert season like "2023/2024" to "2324"
    season_part = season.split("/")[1][-2:]
    year_before = season.split("/")[0][-2:]
    season_code = year_before + season_part
    
    return f"https://www.football-data.co.uk/mmz4281/{season_code}/{league_code}.csv"


@st.cache_data(ttl=300)
def get_available_seasons(league: str) -> list[str]:
    """Get available seasons for a league (cached 5 min)."""
    # Updated to include 2025/2026 from feature/streamlit-dashboard
    return [f"{y}/{y+1}" for y in range(2020, 2026)]


def get_team_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate team statistics from match data."""
    if df.empty:
        return pd.DataFrame()
    
    # Ensure required columns exist
    required = ['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
    if not all(col in df.columns for col in required):
        return pd.DataFrame()
    
    teams = set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique())
    stats = []
    
    for team in teams:
        home = df[df['HomeTeam'] == team]
        away = df[df['AwayTeam'] == team]
        
        # Home stats
        home_wins = len(home[home['FTR'] == 'H'])
        home_draws = len(home[home['FTR'] == 'D'])
        home_losses = len(home[home['FTR'] == 'A'])
        home_gf = home['FTHG'].sum()
        home_ga = home['FTAG'].sum()
        
        # Away stats
        away_wins = len(away[away['FTR'] == 'A'])
        away_draws = len(away[away['FTR'] == 'D'])
        away_losses = len(away[away['FTR'] == 'H'])
        away_gf = away['FTAG'].sum()
        away_ga = away['FTHG'].sum()
        
        # Totals
        played = len(home) + len(away)
        wins = home_wins + away_wins
        draws = home_draws + away_draws
        losses = home_losses + away_losses
        gf = home_gf + away_gf
        ga = home_ga + away_ga
        gd = gf - ga
        pts = wins * 3 + draws
        
        stats.append({
            'Team': team,
            'P': played,
            'W': wins,
            'D': draws,
            'L': losses,
            'GF': gf,
            'GA': ga,
            'GD': gd,
            'Pts': pts,
        })
    
    return pd.DataFrame(stats).sort_values(
        ['Pts', 'GD', 'GF'], ascending=[False, False, False]
    ).reset_index(drop=True)
