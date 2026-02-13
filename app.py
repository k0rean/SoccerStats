"""
SoccerStats Web Dashboard
A modern Streamlit dashboard for soccer statistics visualization.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="SoccerStats",
    page_icon="⚽",
    layout="wide"
)

# League codes (from original utils.py)
LEAGUE_CODES = {
    'Premier League': 'E0',
    'La Liga': 'SP1',
    'Bundesliga': 'D1',
    'Serie A': 'I1',
    'Ligue 1': 'F1',
    'Liga NOS': 'P1',
    'Eredivisie': 'N1',
    'Jupiler': 'B1',
    'Turkey': 'T1',
    'Greece': 'G1',
    'Premiership': 'SC0',
    'Championship': 'E1',
    'La Liga2': 'SP2',
    'Bundesliga2': 'D2',
    'Serie B': 'I2',
    'Ligue 2': 'F2'
}

# Current season
CURRENT_SEASON = "2024/2025"

def download_league_data(league: str, year: str = CURRENT_SEASON) -> pd.DataFrame:
    """Download league data from football-data.co.uk"""
    import urllib.request
    import os
    
    filename = LEAGUE_CODES[league] + ".csv"
    year_str = year.replace('/', '')
    url = f'http://www.football-data.co.uk/mmz4281/{year_str}/{filename}'
    
    cache_dir = "data/cache"
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{league}_{year}.csv")
    
    if os.path.exists(cache_file):
        return pd.read_csv(cache_file)
    
    try:
        urllib.request.urlretrieve(url, cache_file)
        return pd.read_csv(cache_file)
    except Exception as e:
        st.error(f"Failed to download data for {league}: {e}")
        return pd.DataFrame()

def calculate_team_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate team statistics from match data."""
    teams = set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique())
    stats = []
    
    for team in teams:
        # Home games
        home_games = df[df['HomeTeam'] == team]
        # Away games
        away_games = df[df['AwayTeam'] == team]
        
        # Results
        home_wins = len(home_games[home_games['FTR'] == 'H'])
        home_draws = len(home_games[home_games['FTR'] == 'D'])
        home_losses = len(home_games[home_games['FTR'] == 'A'])
        
        away_wins = len(away_games[away_games['FTR'] == 'A'])
        away_draws = len(away_games[away_games['FTR'] == 'D'])
        away_losses = len(away_games[away_games['FTR'] == 'H'])
        
        total_wins = home_wins + away_wins
        total_draws = home_draws + away_draws
        total_losses = home_losses + away_losses
        total_games = total_wins + total_draws + total_losses
        
        points = total_wins * 3 + total_draws * 1
        
        # Goals
        home_scored = home_games['FTHG'].sum()
        home_conceded = home_games['FTAG'].sum()
        away_scored = away_games['FTAG'].sum()
        away_conceded = away_games['FTHG'].sum()
        
        stats.append({
            'Team': team,
            'Played': total_games,
            'Won': total_wins,
            'Drawn': total_draws,
            'Lost': total_losses,
            'Points': points,
            'GF': home_scored + away_scored,
            'GA': home_conceded + away_conceded,
            'GD': (home_scored + away_scored) - (home_conceded + away_conceded),
            'PPG': round(points / total_games, 2) if total_games > 0 else 0,
            'Home Wins': home_wins,
            'Away Wins': away_wins,
        })
    
    return pd.DataFrame(stats).sort_values('Points', ascending=False).reset_index(drop=True)

def main():
    st.title("⚽ SoccerStats Dashboard")
    st.markdown("Historical soccer data analysis tool")
    
    # Sidebar
    st.sidebar.header("Settings")
    
    # League selection
    selected_league = st.sidebar.selectbox(
        "Select League",
        list(LEAGUE_CODES.keys())
    )
    
    # Season selection
    seasons = [f"{y}/{y+1}" for y in range(2015, 2025)]
    selected_season = st.sidebar.selectbox(
        "Select Season",
        seasons,
        index=seasons.index(CURRENT_SEASON) if CURRENT_SEASON in seasons else 9
    )
    
    # Load data
    with st.spinner(f'Loading {selected_league} data...'):
        df = download_league_data(selected_leason, selected_season)
    
    if df.empty:
        st.warning("No data available for selected league/season.")
        return
    
    # Calculate stats
    team_stats = calculate_team_stats(df)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 League Table", "⚽ Goals", "📊 Analytics", "📈 Trends"])
    
    with tab1:
        st.subheader(f"{selected_league} - {selected_season}")
        
        # Styled table
        st.dataframe(
            team_stats[['Team', 'Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points']],
            use_container_width=True,
            hide_index=True
        )
        
        # Points chart
        fig = px.bar(
            team_stats.head(10), 
            x='Team', 
            y='Points',
            color='Points',
            color_continuous_scale='RdYlGn',
            title='Top 10 Teams by Points'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Goals For")
            fig_gf = px.bar(
                team_stats.sort_values('GF', ascending=False).head(10),
                x='Team',
                y='GF',
                color='GF',
                color_continuous_scale='Greens',
                title='Top 10 - Goals For'
            )
            st.plotly_chart(fig_gf, use_container_width=True)
        
        with col2:
            st.subheader("Goals Against")
            fig_ga = px.bar(
                team_stats.sort_values('GA', ascending=True).head(10),
                x='Team',
                y='GA',
                color='GA',
                color_continuous_scale='Reds_r',
                title='Top 10 - Least Goals Conceded'
            )
            st.plotly_chart(fig_ga, use_container_width=True)
    
    with tab3:
        st.subheader("Team Analytics")
        
        # Team comparison
        teams = st.multiselect(
            "Select Teams to Compare",
            team_stats['Team'].tolist(),
            default=team_stats['Team'].tolist()[:3]
        )
        
        if teams:
            compare_df = team_stats[team_stats['Team'].isin(teams)]
            
            fig = go.Figure(data=[
                go.Bar(name='Won', x=compare_df['Team'], y=compare_df['Won']),
                go.Bar(name='Drawn', x=compare_df['Team'], y=compare_df['Drawn']),
                go.Bar(name='Lost', x=compare_df['Team'], y=compare_df['Lost'])
            ])
            fig.update_layout(barmode='group', title='Wins/Draws/Losses Comparison')
            st.plotly_chart(fig, use_container_width=True)
        
        # Points per game
        fig_ppg = px.scatter(
            team_stats,
            x='Played',
            y='Points',
            size='GD',
            hover_name='Team',
            color='Points',
            color_continuous_scale='RdYlGn',
            title='Points vs Games Played'
        )
        st.plotly_chart(fig_ppg, use_container_width=True)
    
    with tab4:
        st.subheader("Performance Trends")
        
        # Select team
        team = st.selectbox("Select Team", team_stats['Team'].tolist())
        
        team_data = team_stats[team_stats['Team'] == team].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Points", team_data['Points'])
        col2.metric("Goal Difference", team_data['GD'])
        col3.metric("Points Per Game", team_data['PPG'])
        col4.metric("Win Rate", f"{round(team_data['Won']/team_data['Played']*100, 1)}%" if team_data['Played'] > 0 else "0%")
        
        # Win breakdown
        fig_wins = go.Figure(data=[
            go.Pie(
                labels=['Home Wins', 'Away Wins', 'Draws', 'Home Losses', 'Away Losses'],
                values=[
                    team_data['Home Wins'],
                    team_data['Away Wins'],
                    team_data['Drawn'],
                    team_data['Lost'] - team_data['Away Wins'],
                    team_data['Lost'] - team_data['Home Wins']
                ],
                hole=0.4
            )
        ])
        fig_wins.update_layout(title=f'{team} - Performance Breakdown')
        st.plotly_chart(fig_wins, use_container_width=True)

if __name__ == "__main__":
    main()
