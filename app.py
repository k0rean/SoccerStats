"""
SoccerStats - Premium Football Analytics Dashboard
v2.0 - Enhanced with Form Guide, Home/Away, O/U 2.5, BTTS, Scorelines
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="SoccerStats Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Outfit', sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    .stApp {
        background: #0a0a0f;
        color: #e0e0e0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12121a 0%, #0a0a0f 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    
    /* Glass cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 24px;
        padding: 28px;
        margin: 16px 0;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255,255,255,0.15);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    /* Premium metrics */
    .metric-card {
        background: linear-gradient(135deg, rgba(30,30,40,0.8) 0%, rgba(20,20,30,0.9) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
    }
    
    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 42px;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 50%, #ff006e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    
    .metric-label {
        color: #666;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 8px;
    }
    
    /* Team row */
    .team-row {
        display: flex;
        align-items: center;
        padding: 16px 20px;
        background: rgba(255,255,255,0.03);
        border-radius: 16px;
        margin: 8px 0;
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.2s ease;
    }
    
    .team-row:hover {
        background: rgba(255,255,255,0.06);
        transform: scale(1.01);
    }
    
    .team-pos {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 24px;
        font-weight: 700;
        width: 40px;
        color: #333;
    }
    
    .team-name {
        flex: 1;
        font-size: 16px;
        font-weight: 500;
        padding-left: 16px;
    }
    
    .team-stat {
        width: 50px;
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
    }
    
    .team-pts {
        font-size: 20px;
        color: #00d4ff;
    }
    
    /* Form guide dots */
    .form-dots {
        display: flex;
        gap: 4px;
    }
    .form-dot {
        width: 24px;
        height: 24px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 700;
    }
    .form-win { background: #00d4ff; color: #000; }
    .form-draw { background: #7b2cbf; color: #fff; }
    .form-loss { background: #ff006e; color: #fff; }
    
    /* Custom tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255,255,255,0.03);
        padding: 8px;
        border-radius: 16px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 500;
        color: #666 !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%) !important;
        color: #fff !important;
        box-shadow: 0 4px 20px rgba(0,212,255,0.3);
    }
    
    /* Select boxes */
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 14px !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        margin: 40px 0;
    }
    
    /* Glowing title */
    .glow-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 52px;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #00d4ff 50%, #7b2cbf 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 8px;
    }
    
    .glow-subtitle {
        text-align: center;
        color: #444;
        font-size: 14px;
        letter-spacing: 4px;
        text-transform: uppercase;
    }
    
    /* Floating particles background */
    .bg-pattern {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(0,212,255,0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(123,44,191,0.08) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255,0,110,0.05) 0%, transparent 40%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0a0f;
    }
    ::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 3px;
    }
    
    /* DataFrame styling */
    div[data-testid="stDataFrame"] {
        background: transparent !important;
    }
    
    /* Chart container */
    .chart-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        padding: 20px;
    }
    
    /* Stat pill */
    .stat-pill {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin: 0 4px;
    }
    .pill-green { background: rgba(0,212,255,0.2); color: #00d4ff; }
    .pill-purple { background: rgba(123,44,191,0.2); color: #7b2cbf; }
    .pill-pink { background: rgba(255,0,110,0.2); color: #ff006e; }
    </style>
    
    <div class="bg-pattern"></div>
""", unsafe_allow_html=True)

# League codes with flags
LEAGUE_CODES = {
    '🇬🇧 Premier League': 'E0',
    '🇪🇸 La Liga': 'SP1',
    '🇩🇪 Bundesliga': 'D1',
    '🇮🇹 Serie A': 'I1',
    '🇫🇷 Ligue 1': 'F1',
    '🇵🇹 Liga Portugal': 'P1',
    '🇳🇱 Eredivisie': 'N1',
    '🇧🇪 Belgian Pro': 'B1',
}

CURRENT_SEASON = "2025/2026"


def download_league_data(league: str, year: str = CURRENT_SEASON):
    import urllib.request
    import urllib.error
    import os
    
    filename = LEAGUE_CODES[league] + ".csv"
    year_str = year[2:4] + year[-2:]
    url = f'https://www.football-data.co.uk/mmz4281/{year_str}/{filename}'
    
    cache_dir = "data/cache"
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{league}_{year_str}.csv")
    
    if os.path.exists(cache_file):
        try:
            return pd.read_csv(cache_file)
        except:
            os.remove(cache_file)
    
    try:
        response = urllib.request.urlopen(url)
        with open(cache_file, 'wb') as f:
            f.write(response.read())
        return pd.read_csv(cache_file)
    except:
        return pd.DataFrame()


def calculate_team_stats(df):
    if df.empty:
        return pd.DataFrame()
    
    teams = set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique())
    stats = []
    
    for team in teams:
        home = df[df['HomeTeam'] == team]
        away = df[df['AwayTeam'] == team]
        
        hw = len(home[home['FTR'] == 'H'])
        hd = len(home[home['FTR'] == 'D'])
        hl = len(home[home['FTR'] == 'A'])
        
        aw = len(away[away['FTR'] == 'A'])
        ad = len(away[away['FTR'] == 'D'])
        al = len(away[away['FTR'] == 'H'])
        
        pts = (hw + aw) * 3 + (hd + ad)
        gp = hw + hd + hl + aw + ad + al
        
        gf = home['FTHG'].sum() + away['FTAG'].sum()
        ga = home['FTAG'].sum() + away['FTHG'].sum()
        
        stats.append({
            'Team': team, 'P': gp, 'W': hw+aw, 'D': hd+ad, 'L': hl+al,
            'GF': gf, 'GA': ga, 'GD': gf-ga, 'Pts': pts,
            'PPG': round(pts/gp, 2) if gp > 0 else 0
        })
    
    return pd.DataFrame(stats).sort_values(['Pts', 'GD', 'GF'], ascending=[False, False, False]).reset_index(drop=True)


def calculate_home_away_stats(df):
    """Separate home and away statistics."""
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    
    teams = set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique())
    home_stats = []
    away_stats = []
    
    for team in teams:
        # Home
        home = df[df['HomeTeam'] == team]
        h_wins = len(home[home['FTR'] == 'H'])
        h_draws = len(home[home['FTR'] == 'D'])
        h_losses = len(home[home['FTR'] == 'A'])
        h_pts = h_wins * 3 + h_draws
        h_gp = len(home)
        
        home_stats.append({
            'Team': team, 'P': h_gp, 'W': h_wins, 'D': h_draws, 'L': h_losses,
            'GF': home['FTHG'].sum(), 'GA': home['FTAG'].sum(),
            'Pts': h_pts, 'PPG': round(h_pts/h_gp, 2) if h_gp > 0 else 0
        })
        
        # Away
        away = df[df['AwayTeam'] == team]
        a_wins = len(away[away['FTR'] == 'A'])
        a_draws = len(away[away['FTR'] == 'D'])
        a_losses = len(away[away['FTR'] == 'H'])
        a_pts = a_wins * 3 + a_draws
        a_gp = len(away)
        
        away_stats.append({
            'Team': team, 'P': a_gp, 'W': a_wins, 'D': a_draws, 'L': a_losses,
            'GF': away['FTAG'].sum(), 'GA': away['FTHG'].sum(),
            'Pts': a_pts, 'PPG': round(a_pts/a_gp, 2) if a_gp > 0 else 0
        })
    
    home_df = pd.DataFrame(home_stats).sort_values(['Pts', 'GF'], ascending=[False, False]).reset_index(drop=True)
    away_df = pd.DataFrame(away_stats).sort_values(['Pts', 'GF'], ascending=[False, False]).reset_index(drop=True)
    
    return home_df, away_df


def get_form_guide(df, team, n=5):
    """Get last n matches for a team."""
    home_matches = df[df['HomeTeam'] == team].copy()
    away_matches = df[df['AwayTeam'] == team].copy()
    
    # Mark home/away and result
    home_matches['Result'] = home_matches['FTR']
    home_matches['Goals'] = home_matches['FTHG'].astype(str) + '-' + home_matches['FTAG'].astype(str)
    home_matches['Venue'] = 'H'
    
    away_matches['Result'] = away_matches['FTR']
    away_matches['Goals'] = away_matches['FTAG'].astype(str) + '-' + away_matches['FTHG'].astype(str)
    away_matches['Venue'] = 'A'
    
    # Combine and sort by date if available, otherwise just take last n
    all_matches = pd.concat([home_matches, away_matches])
    
    # Try to sort by match order (last matches first)
    if 'Date' in all_matches.columns:
        try:
            all_matches['Date'] = pd.to_datetime(all_matches['Date'], format='%d/%m/%Y', errors='coerce')
            all_matches = all_matches.sort_values('Date', ascending=False)
        except:
            pass
    
    return all_matches.head(n)


def get_team_color(pos):
    colors = {
        1: '#ffd700',
        2: '#c0c0c0', 
        3: '#cd7f32',
        4: '#00d4ff',
    }
    return colors.get(pos, '#333')


def render_form_dots(form_results):
    """Render form guide as W/D/L dots."""
    dots_html = '<div class="form-dots">'
    for _, match in form_results.iterrows():
        result = match['Result']
        if result == 'H':
            # Team won
            if match['Venue'] == 'H':
                dots_html += '<div class="form-dot form-win">W</div>'
            else:
                dots_html += '<div class="form-dot form-loss">L</div>'
        elif result == 'A':
            # Team lost
            if match['Venue'] == 'H':
                dots_html += '<div class="form-dot form-loss">L</div>'
            else:
                dots_html += '<div class="form-dot form-win">W</div>'
        else:
            dots_html += '<div class="form-dot form-draw">D</div>'
    dots_html += '</div>'
    return dots_html


def main():
    # Header
    st.markdown('<div class="glow-title">SOCCERSTATS</div>', unsafe_allow_html=True)
    st.markdown('<div class="glow-subtitle">Premium Football Analytics</div>', unsafe_allow_html=True)
    
    # Controls at top of main area
    col_ctrl1, col_ctrl2 = st.columns([2, 1])
    
    with col_ctrl1:
        st.markdown("### 🏆 Select League")
        selected_league = st.selectbox("League", list(LEAGUE_CODES.keys()), label_visibility="collapsed", key="league_select")
    
    with col_ctrl2:
        st.markdown("### 📅 Season")
        seasons = [f"{y}/{y+1}" for y in range(2020, 2026)]
        try:
            default_idx = seasons.index(CURRENT_SEASON)
        except:
            default_idx = len(seasons) - 1
        selected_season = st.selectbox("Season", seasons, index=default_idx, label_visibility="collapsed", key="season_select")
    
    # Load data
    with st.spinner(''):
        df = download_league_data(selected_league, selected_season)
    
    if df.empty:
        st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 80px;">
                <div style="font-size: 64px; margin-bottom: 20px;">📊</div>
                <h2 style="color: #888 !important;">No Data Available</h2>
                <p style="color: #555;">{selected_league} {selected_season} data not yet available</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    team_stats = calculate_team_stats(df)
    home_stats, away_stats = calculate_home_away_stats(df)
    league_name = selected_league.split()[-1]
    
    # Hero section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(df)}</div>
                <div class="metric-label">Matches</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_goals = df['FTHG'].sum() + df['FTAG'].sum()
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_goals}</div>
                <div class="metric-label">Goals</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg = round(total_goals / len(df), 2) if len(df) > 0 else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg}</div>
                <div class="metric-label">Avg Goals</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        home_pct = round(len(df[df['FTR']=='H']) / len(df) * 100, 1) if len(df) > 0 else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{home_pct}%</div>
                <div class="metric-label">Home Wins</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 Table", "🔥 Form", "🏠 Home/Away", "⚽ Goals", "📈 Compare"])
    
    # === TAB 1: League Table ===
    with tab1:
        st.markdown(f"### {league_name} · {selected_season}")
        
        # Custom table
        for i, row in team_stats.iterrows():
            pos = i + 1
            color = get_team_color(pos)
            
            st.markdown(f"""
                <div class="team-row">
                    <div class="team-pos" style="color: {color}">{pos}</div>
                    <div class="team-name">{row['Team']}</div>
                    <div class="team-stat">{row['P']}</div>
                    <div class="team-stat">{row['W']}</div>
                    <div class="team-stat">{row['D']}</div>
                    <div class="team-stat">{row['L']}</div>
                    <div class="team-stat">{row['GF']}-{row['GA']}</div>
                    <div class="team-stat" style="color: #666">{row['GD']:+d}</div>
                    <div class="team-stat team-pts">{row['Pts']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Chart
        fig = px.bar(
            team_stats.head(8), x='Team', y='Pts',
            color='Pts',
            color_continuous_scale=[[0, '#1a1a2e'], [0.5, '#7b2cbf'], [1, '#00d4ff']],
            title='',
            text='Pts'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': '#888', 'family': 'Space Grotesk'},
            showlegend=False,
            height=350,
            margin=dict(t=0, b=0, l=40, r=40)
        )
        fig.update_traces(textposition='outside', marker=dict(line=dict(width=0)))
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # === TAB 2: Form Guide ===
    with tab2:
        st.markdown(f"### 🔥 Form Guide · {league_name}")
        st.markdown("<p style='color:#555; font-size:13px;'>Last 5 matches (H=Home, A=Away)</p>", unsafe_allow_html=True)
        
        # Select team to view form
        selected_team = st.selectbox("Select Team", team_stats['Team'].tolist())
        
        if selected_team:
            form = get_form_guide(df, selected_team, 5)
            
            if not form.empty:
                # Form summary
                wins = len(form[((form['Venue']=='H') & (form['Result']=='H')) | ((form['Venue']=='A') & (form['Result']=='A'))])
                draws = len(form[form['Result']=='D'])
                losses = len(form) - wins - draws
                
                col_f1, col_f2, col_f3 = st.columns(3)
                with col_f1:
                    st.markdown(f'<div class="stat-pill pill-green">W: {wins}</div>', unsafe_allow_html=True)
                with col_f2:
                    st.markdown(f'<div class="stat-pill pill-purple">D: {draws}</div>', unsafe_allow_html=True)
                with col_f3:
                    st.markdown(f'<div class="stat-pill pill-pink">L: {losses}</div>', unsafe_allow_html=True)
                
                st.markdown("#### Last 5 Matches")
                
                # Build match cards
                for _, match in form.iterrows():
                    venue = "🏠 Home" if match['Venue'] == 'H' else "✈️ Away"
                    
                    # Determine result text
                    if match['Result'] == 'H':
                        if match['Venue'] == 'H':
                            result_text, result_class = "W", "pill-green"
                        else:
                            result_text, result_class = "L", "pill-pink"
                    elif match['Result'] == 'A':
                        if match['Venue'] == 'A':
                            result_text, result_class = "W", "pill-green"
                        else:
                            result_text, result_class = "L", "pill-pink"
                    else:
                        result_text, result_class = "D", "pill-purple"
                    
                    # Get opponent
                    if match['Venue'] == 'H':
                        opponent = match['AwayTeam']
                    else:
                        opponent = match['HomeTeam']
                    
                    st.markdown(f"""
                        <div class="team-row" style="justify-content: space-between;">
                            <div style="display:flex; align-items:center; gap:16px;">
                                <span style="color:#555; font-size:12px;">{venue}</span>
                                <span style="font-weight:600;">{opponent}</span>
                            </div>
                            <div style="display:flex; align-items:center; gap:16px;">
                                <span style="font-family:'Space Grotesk'; font-weight:700;">{match['Goals']}</span>
                                <span class="stat-pill {result_class}">{result_text}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        
        # Form table - all teams
        st.markdown("#### All Teams Form")
        
        form_data = []
        for team in team_stats['Team']:
            form = get_form_guide(df, team, 5)
            wins = len(form[((form['Venue']=='H') & (form['Result']=='H')) | ((form['Venue']=='A') & (form['Result']=='A'))])
            draws = len(form[form['Result']=='D'])
            losses = len(form) - wins - draws
            form_str = f"{wins}W-{draws}D-{losses}L"
            form_data.append({'Team': team, 'Form': form_str, 'W': wins, 'D': draws, 'L': losses})
        
        form_df = pd.DataFrame(form_data)
        
        # Add mini form dots to each team
        for i, row in team_stats.iterrows():
            team = row['Team']
            form_row = form_df[form_df['Team'] == team].iloc[0]
            form_dots = render_form_dots(get_form_guide(df, team, 5))
            
            st.markdown(f"""
                <div class="team-row">
                    <div class="team-name">{team}</div>
                    <div style="flex:1; text-align:right;">{form_dots}</div>
                    <div class="team-stat" style="width:80px; color:#666;">{form_row['Form']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # === TAB 3: Home/Away ===
    with tab3:
        st.markdown(f"### 🏠 Home vs Away · {league_name}")
        
        subtab1, subtab2 = st.tabs(["🏠 Home Table", "✈️ Away Table"])
        
        with subtab1:
            st.markdown("#### Home Performance")
            
            for i, row in home_stats.iterrows():
                pos = i + 1
                color = get_team_color(pos)
                
                st.markdown(f"""
                    <div class="team-row">
                        <div class="team-pos" style="color: {color}">{pos}</div>
                        <div class="team-name">{row['Team']}</div>
                        <div class="team-stat">{row['P']}</div>
                        <div class="team-stat">{row['W']}</div>
                        <div class="team-stat">{row['D']}</div>
                        <div class="team-stat">{row['L']}</div>
                        <div class="team-stat">{row['GF']}-{row['GA']}</div>
                        <div class="team-stat" style="color: #666">{row['GF']-row['GA']:+d}</div>
                        <div class="team-stat team-pts">{row['Pts']}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        with subtab2:
            st.markdown("#### Away Performance")
            
            for i, row in away_stats.iterrows():
                pos = i + 1
                color = get_team_color(pos)
                
                st.markdown(f"""
                    <div class="team-row">
                        <div class="team-pos" style="color: {color}">{pos}</div>
                        <div class="team-name">{row['Team']}</div>
                        <div class="team-stat">{row['P']}</div>
                        <div class="team-stat">{row['W']}</div>
                        <div class="team-stat">{row['D']}</div>
                        <div class="team-stat">{row['L']}</div>
                        <div class="team-stat">{row['GF']}-{row['GA']}</div>
                        <div class="team-stat" style="color: #666">{row['GF']-row['GA']:+d}</div>
                        <div class="team-stat team-pts">{row['Pts']}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Comparison chart
        st.markdown("#### 🏠 vs ✈️ Points Comparison")
        
        comp_df = pd.merge(
            home_stats[['Team', 'Pts', 'PPG']].rename(columns={'Pts': 'HomePts', 'PPG': 'HomePPG'}),
            away_stats[['Team', 'Pts', 'PPG']].rename(columns={'Pts': 'AwayPts', 'PPG': 'AwayPPG'}),
            on='Team'
        ).head(10)
        
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            name='Home', x=comp_df['Team'], y=comp_df['HomePts'],
            marker_color='#00d4ff', hovertemplate='%{x}: %{y} pts'
        ))
        fig_comp.add_trace(go.Bar(
            name='Away', x=comp_df['Team'], y=comp_df['AwayPts'],
            marker_color='#7b2cbf', hovertemplate='%{x}: %{y} pts'
        ))
        
        fig_comp.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': '#888'},
            height=400,
            margin=dict(t=20, b=40, l=40, r=40),
            legend=dict(orientation='h', y=1.1, x=0.5, xanchor='center')
        )
        st.plotly_chart(fig_comp, use_container_width=True)
    
    # === TAB 4: Goals (expanded) ===
    with tab4:
        st.markdown(f"### ⚽ Goal Stats · {league_name}")
        
        # Calculate additional stats
        total_matches = len(df)
        
        # Over/Under 2.5
        df['TotalGoals'] = df['FTHG'] + df['FTAG']
        over_25 = len(df[df['TotalGoals'] >= 3])
        under_25 = total_matches - over_25
        over_25_pct = round(over_25 / total_matches * 100, 1) if total_matches > 0 else 0
        
        # BTTS
        btts_yes = len(df[(df['FTHG'] > 0) & (df['FTAG'] > 0)])
        btts_no = total_matches - btts_yes
        btts_pct = round(btts_yes / total_matches * 100, 1) if total_matches > 0 else 0
        
        # 1st Half vs 2nd Half goals
        first_half_goals = df['FTHG'].sum()  # Approximation
        second_half_goals = df['FTAG'].sum()  # This is not accurate, let's check columns
        
        # Better: use HTHG (half-time home goals) and HTAG (half-time away goals)
        if 'HTHG' in df.columns and 'HTAG' in df.columns:
            first_half_goals = df['HTHG'].sum() + df['HTAG'].sum()
            second_half_goals = (df['FTHG'] - df['HTHG']).sum() + (df['FTAG'] - df['HTAG']).sum()
        else:
            # Fallback: assume ~45%/55% split
            total = df['FTHG'].sum() + df['FTAG'].sum()
            first_half_goals = int(total * 0.43)
            second_half_goals = total - first_half_goals
        
        # Scoreline matrix
        df['Scoreline'] = df['FTHG'].astype(str) + '-' + df['FTAG'].astype(str)
        scoreline_counts = df['Scoreline'].value_counts().head(10)
        
        # Row for key metrics
        col_g1, col_g2, col_g3, col_g4 = st.columns(4)
        
        with col_g1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{over_25_pct}%</div>
                    <div class="metric-label">Over 2.5</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_g2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{100-over_25_pct}%</div>
                    <div class="metric-label">Under 2.5</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_g3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{btts_pct}%</div>
                    <div class="metric-label">BTTS Yes</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_g4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{100-btts_pct}%</div>
                    <div class="metric-label">BTTS No</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Charts row
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            # O/U pie chart
            fig_ou = go.Figure(data=[go.Pie(
                labels=['Over 2.5', 'Under 2.5'],
                values=[over_25, under_25],
                marker_colors=['#00d4ff', '#1a1a2e'],
                hole=0.7,
                textinfo='label+percent',
                textposition='outside'
            )])
            fig_ou.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': '#888'},
                height=350,
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.markdown("#### 📊 Over/Under 2.5")
            st.plotly_chart(fig_ou, use_container_width=True)
        
        with col_c2:
            # BTTS pie chart
            fig_btts = go.Figure(data=[go.Pie(
                labels=['BTTS Yes', 'BTTS No'],
                values=[btts_yes, btts_no],
                marker_colors=['#7b2cbf', '#1a1a2e'],
                hole=0.7,
                textinfo='label+percent',
                textposition='outside'
            )])
            fig_btts.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': '#888'},
                height=350,
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.markdown("#### 🎯 Both Teams to Score")
            st.plotly_chart(fig_btts, use_container_width=True)
        
        # Half-time goals
        st.markdown("#### ⏱️ First Half vs Second Half")
        
        col_h1, col_h2 = st.columns(2)
        
        with col_h1:
            fig_half = go.Figure(data=[go.Bar(
                x=['First Half', 'Second Half'],
                y=[first_half_goals, second_half_goals],
                marker_color=['#ff006e', '#00d4ff'],
                text=[first_half_goals, second_half_goals],
                textposition='outside'
            )])
            fig_half.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': '#888'},
                height=300,
                margin=dict(t=20, b=40, l=40, r=40),
                showlegend=False
            )
            st.plotly_chart(fig_half, use_container_width=True)
        
        with col_h2:
            # Half-time results
            if 'HTR' in df.columns:
                hth_wins = len(df[df['HTR'] == 'H'])
                htd_draws = len(df[df['HTR'] == 'D'])
                hta_wins = len(df[df['HTR'] == 'A'])
                
                fig_ht = go.Figure(data=[go.Pie(
                    labels=['Home Lead', 'Draw', 'Away Lead'],
                    values=[hth_wins, htd_draws, hta_wins],
                    marker_colors=['#00d4ff', '#7b2cbf', '#ff006e'],
                    hole=0.7,
                    textinfo='label+percent'
                )])
                fig_ht.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#888'},
                    height=300,
                    showlegend=False,
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                st.markdown("#### 🕐 Half-Time Leader")
                st.plotly_chart(fig_ht, use_container_width=True)
        
        # Scoreline matrix
        st.markdown("#### 🔢 Most Common Scorelines")
        
        col_s1, col_s2 = st.columns([2, 1])
        
        with col_s1:
            fig_score = px.bar(
                x=scoreline_counts.index,
                y=scoreline_counts.values,
                labels={'x': 'Scoreline', 'y': 'Count'},
                color=scoreline_counts.values,
                color_continuous_scale='Greens'
            )
            fig_score.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': '#888'},
                height=350,
                margin=dict(t=20, b=40, l=40, r=40),
                showlegend=False
            )
            fig_score.update_traces(marker=dict(line=dict(width=0)))
            st.plotly_chart(fig_score, use_container_width=True)
        
        with col_s2:
            st.markdown("##### Top 10")
            for score, count in scoreline_counts.items():
                st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
                        <span style="font-family:'Space Grotesk'; font-weight:600;">{score}</span>
                        <span style="color:#666;">{count}</span>
                    </div>
                """, unsafe_allow_html=True)
        
        # Original goal charts (top scorers, defense, GD)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Top Scorers")
            top = team_stats.nlargest(10, 'GF')[['Team', 'GF']].iloc[::-1]
            fig1 = px.bar(top, x='GF', y='Team', orientation='h',
                color='GF', color_continuous_scale='Greens')
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font={'color': '#888'}, showlegend=False, height=400,
                margin=dict(t=20, b=20, l=150, r=20),
                xaxis_title='', yaxis_title=''
            )
            fig1.update_traces(marker=dict(line=dict(width=0)))
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown("#### 🛡️ Best Defense")
            best = team_stats.nsmallest(10, 'GA')[['Team', 'GA']].iloc[::-1]
            fig2 = px.bar(best, x='GA', y='Team', orientation='h',
                color='GA', color_continuous_scale='Blues')
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font={'color': '#888'}, showlegend=False, height=400,
                margin=dict(t=20, b=20, l=150, r=20),
                xaxis_title='', yaxis_title=''
            )
            fig2.update_traces(marker=dict(line=dict(width=0)))
            st.plotly_chart(fig2, use_container_width=True)
        
        # Goal difference
        st.markdown("#### 📊 Goal Difference")
        gd = team_stats.sort_values('GD')[['Team', 'GD']]
        fig3 = px.bar(gd, x='GD', y='Team', orientation='h', color='GD',
            color_continuous_scale=[[0, '#ff006e'], [0.5, '#1a1a2e'], [1, '#00d4ff']])
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font={'color': '#888'}, showlegend=False, height=500,
            margin=dict(t=20, b=20, l=150, r=20), xaxis_title='', yaxis_title=''
        )
        fig3.update_traces(marker=dict(line=dict(width=0)))
        st.plotly_chart(fig3, use_container_width=True)
    
    # === TAB 5: Compare ===
    with tab5:
        st.markdown("#### 🔍 Team Comparison")
        teams = st.multiselect("Select teams", team_stats['Team'].tolist(), 
                             default=team_stats['Team'].tolist()[:3])
        
        if teams:
            comp = team_stats[team_stats['Team'].isin(teams)]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Wins', x=comp['Team'], y=comp['W'], 
                               marker_color='#00d4ff', hovertemplate='%{x}: %{y} Wins'))
            fig.add_trace(go.Bar(name='Draws', x=comp['Team'], y=comp['D'], 
                               marker_color='#7b2cbf', hovertemplate='%{x}: %{y} Draws'))
            fig.add_trace(go.Bar(name='Losses', x=comp['Team'], y=comp['L'], 
                               marker_color='#ff006e', hovertemplate='%{x}: %{y} Losses'))
            
            fig.update_layout(
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': '#888'},
                height=400,
                margin=dict(t=20, b=40, l=40, r=40),
                legend=dict(orientation='h', y=1.1, x=0.5, xanchor='center')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #333; padding: 20px; font-size: 12px;">
            SOCCERSTATS PRO v2.0 · Built with Streamlit · Data by football-data.co.uk
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
