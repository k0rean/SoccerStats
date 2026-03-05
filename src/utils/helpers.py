"""Utility functions for SoccerStats."""
import pandas as pd


def get_form_color(result: str) -> str:
    """Get color for form guide result."""
    colors = {'W': '#00d4ff', 'D': '#7b2cbf', 'L': '#ff006e'}
    return colors.get(result, '#666')


def format_position(pos: int) -> str:
    """Format league position with medal for top 3."""
    medals = {1: '🥇', 2: '🥈', 3: '🥉'}
    return medals.get(pos, str(pos))


def calculate_form_guide(df: pd.DataFrame, team: str, n: int = 5) -> list:
    """Calculate recent form for a team (last n matches)."""
    if df.empty:
        return []
    
    home = df[df['HomeTeam'] == team].copy()
    away = df[df['AwayTeam'] == team].copy()
    
    # Add result column
    home['Result'] = home['FTR'].apply(lambda x: 'W' if x == 'H' else ('D' if x == 'D' else 'L'))
    away['Result'] = away['FTR'].apply(lambda x: 'W' if x == 'A' else ('D' if x == 'D' else 'L'))
    
    # Combine and sort by date
    matches = pd.concat([
        home[['Date', 'Result', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']],
        away[['Date', 'Result', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
    ])
    
    if 'Date' in matches.columns:
        try:
            matches['Date'] = pd.to_datetime(matches['Date'], format='%d/%m/%Y', errors='coerce')
            matches = matches.sort_values('Date', ascending=False)
        except Exception:
            pass
    
    return matches['Result'].head(n).tolist()


def calculate_over_under(df: pd.DataFrame, threshold: float = 2.5) -> dict:
    """Calculate Over/Under 2.5 goals stats."""
    if df.empty:
        return {'over': 0, 'under': 0, 'over_pct': 0}
    
    total_goals = df['FTHG'] + df['FTAG']
    over = len(total_goals[total_goals > threshold])
    under = len(total_goals[total_goals <= threshold])
    total = over + under
    
    return {
        'over': over,
        'under': under,
        'over_pct': round(over / total * 100, 1) if total > 0 else 0
    }


def calculate_btts(df: pd.DataFrame) -> dict:
    """Calculate Both Teams To Score stats."""
    if df.empty:
        return {'yes': 0, 'no': 0, 'yes_pct': 0, 'no_pct': 0}
    
    btts_yes = len(df[(df['FTHG'] > 0) & (df['FTAG'] > 0)])
    btts_no = len(df) - btts_yes
    total = len(df)
    yes_pct = round(btts_yes / total * 100, 1) if total > 0 else 0
    
    return {
        'yes': btts_yes,
        'no': btts_no,
        'yes_pct': yes_pct,
        'no_pct': round(100 - yes_pct, 1),
    }


def get_scoreline_counts(df: pd.DataFrame) -> dict:
    """Get most common scorelines."""
    if df.empty:
        return {}
    
    scores = df['FTHG'].astype(str) + ' - ' + df['FTAG'].astype(str)
    return scores.value_counts().head(10).to_dict()
