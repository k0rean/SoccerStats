"""
SoccerStats - Premium Football Analytics Dashboard
v2.2 - Custom website styling, no Streamlit look
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data.loader import (
    LEAGUE_URLS,
    load_match_data,
    get_available_seasons,
    get_team_stats,
)
from src.utils.helpers import (
    get_form_color,
    format_position,
    calculate_form_guide,
    calculate_over_under,
    calculate_btts,
    get_scoreline_counts,
)

# Page config
st.set_page_config(
    page_title="SoccerStats Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide ALL Streamlit chrome - aggressive approach
st.markdown("""
    <style>
    /* Hide everything */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    
    /* Remove top padding */
    .stApp > div:first-child {
        padding-top: 0 !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {width: 8px; height: 8px;}
    ::-webkit-scrollbar-track {background: #0a0a0f;}
    ::-webkit-scrollbar-thumb {background: #333; border-radius: 4px;}
    ::-webkit-scrollbar-thumb:hover {background: #555;}
    
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Outfit', sans-serif !important; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Space Grotesk', sans-serif !important; }
    
    body { background: #0a0a0f; color: #e0e0e0; }
    .stApp { background: #0a0a0f; }
    
    /* Custom Navigation */
    .nav-container {
        background: linear-gradient(90deg, #0f0f17 0%, #1a1a2e 100%);
        padding: 20px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .nav-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 50%, #ff006e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .nav-logo span { font-size: 32px; }
    
    .nav-links {
        display: flex;
        gap: 8px;
    }
    
    .nav-link {
        padding: 12px 24px;
        border-radius: 12px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s ease;
        background: transparent;
        color: #888;
        border: none;
    }
    
    .nav-link:hover { background: rgba(255,255,255,0.05); color: #fff; }
    
    .nav-link.active {
        background: linear-gradient(135deg, rgba(0,212,255,0.15) 0%, rgba(123,44,191,0.15) 100%);
        color: #00d4ff;
        border: 1px solid rgba(0,212,255,0.3);
    }
    
    /* Filters bar */
    .filters-bar {
        background: #12121a;
        padding: 20px 40px;
        display: flex;
        gap: 20px;
        align-items: center;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .filter-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .filter-label {
        color: #666;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Custom selects */
    .filter-select {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        color: #fff !important;
        font-size: 14px !important;
    }
    
    /* Content area */
    .content {
        padding: 40px;
        max-width: 1600px;
        margin: 0 auto;
    }
    
    /* Cards */
    .card {
        background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    .card-header {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* League table row */
    .table-row {
        display: flex;
        align-items: center;
        padding: 16px 20px;
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        margin: 8px 0;
        transition: all 0.2s ease;
    }
    
    .table-row:hover {
        background: rgba(255,255,255,0.05);
        transform: translateX(4px);
    }
    
    .table-pos {
        width: 50px;
        font-weight: 700;
        font-size: 18px;
    }
    
    .table-pos.gold { color: #ffd700; }
    .table-pos.silver { color: #c0c0c0; }
    .table-pos.bronze { color: #cd7f32; }
    
    .table-team {
        flex: 1;
        font-weight: 500;
        font-size: 16px;
    }
    
    .table-stat {
        width: 50px;
        text-align: center;
        color: #888;
    }
    
    .table-pts {
        width: 60px;
        text-align: center;
        font-weight: 700;
        color: #00d4ff;
        font-size: 18px;
    }
    
    /* Stats grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    }
    
    .stat-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 36px;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        color: #666;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    
    /* Form guide */
    .form-match {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        background: rgba(255,255,255,0.02);
        border-radius: 10px;
        margin: 8px 0;
    }
    
    .form-result {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 16px;
        margin-right: 16px;
    }
    
    .form-result.win { background: #00d4ff; color: #000; }
    .form-result.draw { background: #7b2cbf; color: #fff; }
    .form-result.lose { background: #ff006e; color: #fff; }
    
    .form-teams {
        flex: 1;
        font-weight: 500;
    }
    
    .form-score {
        font-weight: 700;
        font-size: 18px;
    }
    
    /* Hide Streamlit elements */
    .stSelectbox > label { display: none; }
    .stSpinner { display: none; }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 40px;
        color: #444;
        font-size: 13px;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin-top: 60px;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'table'


def render_nav():
    """Render custom navigation bar."""
    pages = [
        ('table', '📊 League Table'),
        ('stats', '📈 Statistics'),
        ('form', '🎯 Form Guide'),
        ('betting', '🎰 Betting Stats'),
        ('compare', '⚖️ Compare'),
    ]
    
    nav_html = """
    <div class="nav-container">
        <div class="nav-logo">
            <span>⚽</span> SoccerStats Pro
        </div>
        <div class="nav-links">
    """
    
    for key, label in pages:
        active = 'active' if st.session_state.page == key else ''
        nav_html += f'<button class="nav-link {active}" onclick="parent.postMessage({"type":"streamlit:setComponentValue","value":"{key}"}, "*")">{label}</button>'
    
    nav_html += """
        </div>
    </div>
    """
    
    st.markdown(nav_html, unsafe_allow_html=True)
    
    # Handle nav clicks via Streamlit's component value
    try:
        selected = st.selectbox('Nav', [k for k, _ in pages], 
                               index=[k for k, _ in pages].index(st.session_state.page),
                               label_visibility='collapsed', key='nav_select')
        st.session_state.page = selected
    except:
        pass


def render_filters():
    """Render filters bar."""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        league = st.selectbox("League", list(LEAGUE_URLS.keys()), key='league_filter')
    with col2:
        seasons = get_available_seasons(league)
        season = st.selectbox("Season", seasons, index=len(seasons)-1, key='season_filter')
    
    return league, season


def render_table_page(team_stats):
    """Render league table page."""
    st.markdown('<div class="card"><div class="card-header">🏆 League Table</div>', unsafe_allow_html=True)
    
    for idx, row in team_stats.iterrows():
        pos = idx + 1
        pos_class = 'gold' if pos == 1 else 'silver' if pos == 2 else 'bronze' if pos == 3 else ''
        
        st.markdown(f"""
            <div class="table-row">
                <span class="table-pos {pos_class}">{pos}</span>
                <span class="table-team">{row['Team']}</span>
                <span class="table-stat">{row['P']}</span>
                <span class="table-stat" style="color:#00d4ff">{row['W']}</span>
                <span class="table-stat" style="color:#7b2cbf">{row['D']}</span>
                <span class="table-stat" style="color:#ff006e">{row['L']}</span>
                <span class="table-pts">{row['Pts']}</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_stats_page(team_stats):
    """Render statistics page."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card"><div class="card-header">🎯 Top Scorers</div>', unsafe_allow_html=True)
        top = team_stats.nlargest(10, 'GF')[['Team', 'GF']].iloc[::-1]
        fig1 = px.bar(top, x='GF', y='Team', orientation='h', color='GF', 
                     color_continuous_scale='Greens')
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                          font={'color': '#888'}, showlegend=False, height=400, 
                          margin=dict(t=10, b=10, l=150, r=20))
        fig1.update_traces(marker=dict(line=dict(width=0)))
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card"><div class="card-header">🛡️ Best Defense</div>', unsafe_allow_html=True)
        best = team_stats.nsmallest(10, 'GA')[['Team', 'GA']].iloc[::-1]
        fig2 = px.bar(best, x='GA', y='Team', orientation='h', color='GA', 
                     color_continuous_scale='Blues')
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                          font={'color': '#888'}, showlegend=False, height=400, 
                          margin=dict(t=10, b=10, l=150, r=20))
        fig2.update_traces(marker=dict(line=dict(width=0)))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card"><div class="card-header">📊 Goal Difference</div>', unsafe_allow_html=True)
    gd = team_stats.sort_values('GD')[['Team', 'GD']]
    fig3 = px.bar(gd, x='GD', y='Team', orientation='h', color='GD', 
                 color_continuous_scale=[[0, '#ff006e'], [0.5, '#1a1a2e'], [1, '#00d4ff']])
    fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                      font={'color': '#888'}, showlegend=False, height=500, 
                      margin=dict(t=10, b=10, l=150, r=20))
    fig3.update_traces(marker=dict(line=dict(width=0)))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_form_page(df, team_stats):
    """Render form guide page."""
    teams = team_stats['Team'].tolist()
    selected = st.selectbox("Select Team", teams, key='team_form')
    
    form = calculate_form_guide(df, selected)
    
    if form:
        cols = st.columns(len(form))
        for col, result in zip(cols, form):
            color_class = 'win' if result == 'W' else 'draw' if result == 'D' else 'lose'
            col.markdown(f"""
                <div class="form-result {color_class}">{result}</div>
            """, unsafe_allow_html=True)
    
    # Recent matches
    st.markdown('<div class="card"><div class="card-header">📅 Recent Matches</div>', unsafe_allow_html=True)
    home = df[df['HomeTeam'] == selected].copy()
    away = df[df['AwayTeam'] == selected].copy()
    home['Result'] = home['FTR'].apply(lambda x: 'W' if x == 'H' else ('D' if x == 'D' else 'L'))
    away['Result'] = away['FTR'].apply(lambda x: 'W' if x == 'A' else ('D' if x == 'D' else 'L'))
    
    recent = pd.concat([home, away]).tail(8)
    for _, match in recent.iterrows():
        result_class = 'win' if match['Result'] == 'W' else 'draw' if match['Result'] == 'D' else 'lose'
        st.markdown(f"""
            <div class="form-match">
                <div class="form-result {result_class}">{match['Result']}</div>
                <div class="form-teams">{match['HomeTeam']} vs {match['AwayTeam']}</div>
                <div class="form-score">{match['FTHG']} - {match['FTAG']}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_betting_page(df):
    """Render betting stats page."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card"><div class="card-header">📈 Over/Under 2.5 Goals</div>', unsafe_allow_html=True)
        ou = calculate_over_under(df)
        
        st.markdown(f"""
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{ou['over_pct']}%</div>
                    <div class="stat-label">Over 2.5</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{100 - ou['over_pct']}%</div>
                    <div class="stat-label">Under 2.5</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card"><div class="card-header">🎯 Both Teams To Score</div>', unsafe_allow_html=True)
        btts = calculate_btts(df)
        
        st.markdown(f"""
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{btts['yes_pct']}%</div>
                    <div class="stat-label">BTTS Yes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{btts['no']}%</div>
                    <div class="stat-label">BTTS No</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card"><div class="card-header">⚽ Most Common Scorelines</div>', unsafe_allow_html=True)
    scores = get_scoreline_counts(df)
    for score, count in scores.items():
        st.markdown(f"**{score}** — {count} matches")
    st.markdown('</div>', unsafe_allow_html=True)


def render_compare_page(team_stats):
    """Render comparison page."""
    st.markdown('<div class="card"><div class="card-header">⚖️ Team Comparison</div>', unsafe_allow_html=True)
    
    teams = st.multiselect("Select teams to compare", team_stats['Team'].tolist(), 
                          default=team_stats['Team'].tolist()[:3])
    
    if teams:
        comp = team_stats[team_stats['Team'].isin(teams)]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Wins', x=comp['Team'], y=comp['W'], marker_color='#00d4ff'))
        fig.add_trace(go.Bar(name='Draws', x=comp['Team'], y=comp['D'], marker_color='#7b2cbf'))
        fig.add_trace(go.Bar(name='Losses', x=comp['Team'], y=comp['L'], marker_color='#ff006e'))
        
        fig.update_layout(barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font={'color': '#888'}, height=450, 
                         legend=dict(orientation='h', y=1.1, x=0.5, xanchor='center'))
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    # Render navigation
    render_nav()
    
    # Render filters
    league, season = render_filters()
    
    # Load data
    with st.spinner(f"Loading {league} {season}..."):
        df = load_match_data(league, season)
    
    if df.empty:
        st.error(f"No data for {league} {season}")
        return
    
    # st.success(f"Loaded {len(df)} matches")
    
    team_stats = get_team_stats(df)
    
    if team_stats.empty:
        st.error("Unable to calculate statistics")
        return
    
    # Render current page
    st.markdown('<div class="content">', unsafe_allow_html=True)
    
    if st.session_state.page == 'table':
        render_table_page(team_stats)
    elif st.session_state.page == 'stats':
        render_stats_page(team_stats)
    elif st.session_state.page == 'form':
        render_form_page(df, team_stats)
    elif st.session_state.page == 'betting':
        render_betting_page(df)
    elif st.session_state.page == 'compare':
        render_compare_page(team_stats)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="footer">
            SoccerStats Pro v2.2 · Data by football-data.co.uk
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
