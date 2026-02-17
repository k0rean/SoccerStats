"""
SoccerStats Pro v5.0 - Beautiful & Feature Complete
Combines premium UI with full functionality
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import requests
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="SoccerStats Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Outfit', sans-serif !important; }
    
    h1, h2, h3, h4, h5, h6 { font-family: 'Space Grotesk', sans-serif !important; }
    
    .stApp { background: #0a0a0f; color: #e0e0e0; }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12121a 0%, #0a0a0f 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    
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
    
    .glow-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 48px;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #00d4ff 50%, #7b2cbf 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 8px;
    }
    
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
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%) !important;
        color: #fff !important;
    }
    
    .bg-pattern {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(0,212,255,0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(123,44,191,0.08) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a0a0f; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
    
    div[data-testid="stDataFrame"] { background: transparent !important; }
    
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

# ========== DATA LOADING ==========
@st.cache_data
def load_leagues():
    data_dir = '/home/ubuntu/.openclaw/workspace/repos/SoccerStats/data/cache'
    if not os.path.exists(data_dir):
        return {}
    files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and '_2526' in f]
    leagues = {}
    for f in files:
        name = f.replace('.csv', '').replace('_2526', '').strip()
        leagues[name] = pd.read_csv(os.path.join(data_dir, f))
    return leagues

@st.cache_data(ttl=3600)
def get_upcoming_matches(league_code):
    """Fetch upcoming matches from football-data.org"""
    try:
        headers = {'X-Auth-Token': 'f5216301f58e44e09c87610737a249f8'}
        # Map our league names to competition IDs
        comp_map = {
            'Premier League': 'PL',
            'La Liga': 'PD',
            'Bundesliga': 'BL1',
            'Serie A': 'SA',
            'Ligue 1': 'FL1',
            'Liga Portugal': 'PO'
        }
        comp_id = comp_map.get(league_code, 'PL')
        r = requests.get(f'https://api.football-data.org/v4/competitions/{comp_id}/matches?status=SCHEDULED', headers=headers)
        if r.status_code == 200:
            return r.json().get('matches', [])
    except:
        pass
    return []

def odds_to_prob(odds):
    return 1/odds if odds > 0 else 0

# ========== SIDEBAR ==========
st.sidebar.title("⚽ SoccerStats Pro")
st.sidebar.markdown("---")

# Season toggle
season = st.sidebar.selectbox("Season", ["2025/2026", "2024/2025"], index=0)

# League selector
leagues = load_leagues()
if not leagues:
    st.error("No league data found. Run the data fetcher first.")
    st.stop()

league_names = list(leagues.keys())
selected_league = st.sidebar.selectbox("League", league_names, index=0)

df = leagues[selected_league]

# Convert dates
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
df = df.dropna(subset=['Date'])

# Page selector
pages = [
    "📊 Dashboard",
    "🔮 Predictions", 
    "📈 Form Guide",
    "🤝 Head to Head",
    "🧮 Odds Calculator",
    "🔴 Live",
    "📅 Next Games",
    "💎 Value Bets",
    "📊 Odds Comparison"
]

page = st.sidebar.radio("Page", pages)

# ========== DASHBOARD ==========
if page == "📊 Dashboard":
    st.markdown('<p class="glow-title">⚽ SoccerStats Pro</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center;color:#666;letter-spacing:2px;">{selected_league} • {season}</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df)}</div><div class="metric-label">Matches</div></div>', unsafe_allow_html=True)
    with col2:
        hw = (df['FTR']=='H').sum()
        st.markdown(f'<div class="metric-card"><div class="metric-value">{100*hw/len(df):.1f}%</div><div class="metric-label">Home Wins</div></div>', unsafe_allow_html=True)
    with col3:
        dw = (df['FTR']=='D').sum()
        st.markdown(f'<div class="metric-card"><div class="metric-value">{100*dw/len(df):.1f}%</div><div class="metric-label">Draws</div></div>', unsafe_allow_html=True)
    with col4:
        aw = (df['FTR']=='A').sum()
        st.markdown(f'<div class="metric-card"><div class="metric-value">{100*aw/len(df):.1f}%</div><div class="metric-label">Away Wins</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # League Table
    st.subheader("📊 League Table")
    
    teams = set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique())
    table = []
    for team in teams:
        home = df[df['HomeTeam']==team]
        away = df[df['AwayTeam']==team]
        p = len(home) + len(away)
        w = len(home[df['FTR']=='H']) + len(away[df['FTR']=='A'])
        d = len(home[df['FTR']=='D']) + len(away[df['FTR']=='D'])
        l = len(home[df['FTR']=='A']) + len(away[df['FTR']=='H'])
        gf = home['FTHG'].sum() + away['FTAG'].sum()
        ga = home['FTAG'].sum() + away['FTHG'].sum()
        pts = w*3 + d
        table.append({'Team': team, 'P': p, 'W': w, 'D': d, 'L': l, 'GF': gf, 'GA': ga, 'GD': gf-ga, 'Pts': pts})
    
    table = pd.DataFrame(table).sort_values(['Pts', 'GD', 'GF'], ascending=[False, False, False]).reset_index(drop=True)
    table.index = table.index + 1
    
    st.dataframe(table, use_container_width=True, hide_index=False)
    
    # Recent Results
    st.markdown("---")
    st.subheader("📈 Recent Results")
    
    recent = df.sort_values('Date', ascending=False).head(10)
    for _, r in recent.iterrows():
        date = r['Date'].strftime('%Y-%m-%d')
        if r['FTR'] == 'H':
            result = f"**{r['HomeTeam']}** {r['FTHG']}-{r['FTAG']} {r['AwayTeam']}"
        elif r['FTR'] == 'A':
            result = f"{r['HomeTeam']} {r['FTHG']}-{r['FTAG']} **{r['AwayTeam']}**"
        else:
            result = f"{r['HomeTeam']} {r['FTHG']}-{r['FTAG']} {r['AwayTeam']}"
        st.write(f"{date}: {result}")

# ========== PREDICTIONS ==========
elif page == "🔮 Predictions":
    st.title("🔮 ML Predictions")
    
    if 'B365H' in df.columns:
        dp = df.dropna(subset=['B365H', 'B365D', 'B365A']).copy()
        dp['Prob_H'] = dp['B365H'].apply(odds_to_prob)
        dp['Prob_D'] = dp['B365D'].apply(odds_to_prob)
        dp['Prob_A'] = dp['B365A'].apply(odds_to_prob)
        
        total = dp['Prob_H'] + dp['Prob_D'] + dp['Prob_A']
        dp['Prob_H'] = dp['Prob_H'] / total
        dp['Prob_D'] = dp['Prob_D'] / total
        dp['Prob_A'] = dp['Prob_A'] / total
        
        dp['Pred'] = dp[['Prob_H', 'Prob_D', 'Prob_A']].idxmax(axis=1).map({'Prob_H': 'H', 'Prob_D': 'D', 'Prob_A': 'A'})
        
        correct = (dp['Pred'] == dp['FTR']).sum()
        
        col1, col2 = st.columns(2)
        with col1: st.metric("Total Predictions", len(dp))
        with col2: st.metric("Accuracy", f"{100*correct/len(dp):.1f}%" if len(dp) > 0 else "N/A")
        
        st.divider()
        
        for _, r in dp.sort_values('Date', ascending=False).head(20).iterrows():
            date = r['Date'].strftime('%Y-%m-%d')
            ok = "✅" if r['Pred'] == r['FTR'] else "❌"
            st.write(f"{date}: {r['HomeTeam']} vs {r['AwayTeam']} → **{r['Pred']}** | Actual: {r['FTR']} {ok}")
    else:
        st.warning("No odds data available for predictions")

# ========== FORM GUIDE ==========
elif page == "📈 Form Guide":
    st.title("🔥 Form Guide")
    
    teams = sorted(set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique()))
    selected_team = st.selectbox("Select Team", teams, index=0)
    
    team_matches = df[(df['HomeTeam'] == selected_team) | (df['AwayTeam'] == selected_team)]
    team_matches = team_matches.sort_values('Date', ascending=False).head(10)
    
    # Form calculation
    points = 0
    gf = ga = 0
    form = ""
    
    for _, m in team_matches.iterrows():
        if m['HomeTeam'] == selected_team:
            gf += m['FTHG']
            ga += m['FTAG']
            if m['FTR'] == 'H': points += 3; form += "🟢"
            elif m['FTR'] == 'D': points += 1; form += "🟡"
            else: form += "🔴"
        else:
            gf += m['FTAG']
            ga += m['FTHG']
            if m['FTR'] == 'A': points += 3; form += "🟢"
            elif m['FTR'] == 'D': points += 1; form += "🟡"
            else: form += "🔴"
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Points", points)
    with col2: st.metric("Goals For", gf)
    with col3: st.metric("Goals Against", ga)
    with col4: st.metric("GD", gf-ga)
    
    st.divider()
    st.subheader("Form")
    st.write(form)
    
    st.divider()
    st.subheader("Recent Matches")
    for _, m in team_matches.iterrows():
        date = m['Date'].strftime('%Y-%m-%d')
        if m['HomeTeam'] == selected_team:
            st.write(f"{date}: {selected_team} {m['FTHG']}-{m['FTAG']} vs {m['AwayTeam']}")
        else:
            st.write(f"{date}: {selected_team} {m['FTAG']}-{m['FTHG']} vs {m['HomeTeam']}")

# ========== HEAD TO HEAD ==========
elif page == "🤝 Head to Head":
    st.title("🤝 Head to Head")
    
    teams = sorted(set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique()))
    
    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Team 1", teams, index=0)
    with col2:
        team2 = st.selectbox("Team 2", teams, index=min(1, len(teams)-1))
    
    if team1 and team2:
        h2h = df[((df['HomeTeam'] == team1) & (df['AwayTeam'] == team2)) | 
                  ((df['HomeTeam'] == team2) & (df['AwayTeam'] == team1))]
        h2h = h2h.sort_values('Date', ascending=False)
        
        if len(h2h) > 0:
            t1_wins = len(h2h[(h2h['HomeTeam'] == team1) & (h2h['FTR'] == 'H')]) + len(h2h[(h2h['AwayTeam'] == team1) & (h2h['FTR'] == 'A')])
            t2_wins = len(h2h[(h2h['HomeTeam'] == team2) & (h2h['FTR'] == 'H')]) + len(h2h[(h2h['AwayTeam'] == team2) & (h2h['FTR'] == 'A')])
            draws = len(h2h[h2h['FTR'] == 'D'])
            
            col1, col2, col3 = st.columns(3)
            with col1: st.metric(team1, t1_wins)
            with col2: st.metric("Draws", draws)
            with col3: st.metric(team2, t2_wins)
            
            st.divider()
            for _, r in h2h.head(10).iterrows():
                date = r['Date'].strftime('%Y-%m-%d')
                st.write(f"{date}: {r['HomeTeam']} {r['FTHG']}-{r['FTAG']} {r['AwayTeam']}")
        else:
            st.info("No head-to-head history")

# ========== ODDS CALCULATOR ==========
elif page == "🧮 Odds Calculator":
    st.title("🧮 Odds Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Odds → Probability")
        h = st.number_input("Home Odds", 1.01, 100.0, 1.80)
        d = st.number_input("Draw Odds", 1.01, 100.0, 3.50)
        a = st.number_input("Away Odds", 1.01, 100.0, 4.50)
        if st.button("Calculate"):
            tot = odds_to_prob(h) + odds_to_prob(d) + odds_to_prob(a)
            st.write(f"**Home:** {odds_to_prob(h)/tot*100:.1f}% | **Draw:** {odds_to_prob(d)/tot*100:.1f}% | **Away:** {odds_to_prob(a)/tot*100:.1f}%")
    
    with col2:
        st.subheader("Expected Value")
        yd = st.number_input("Your Odds", 1.01, 100.0, 2.00)
        yp = st.slider("Your Probability %", 0, 100, 50)
        if st.button("Calc EV"):
            ev = (yd * yp/100) - (1 - yp/100)
            st.success(f"EV: {ev*100:.2f}%") if ev > 0 else st.error(f"EV: {ev*100:.2f}%")

# ========== LIVE ==========
elif page == "🔴 Live":
    st.title("🔴 Live Matches")
    
    @st.cache_data(ttl=60)
    def get_live():
        try:
            headers = {'X-Auth-Token': 'f5216301f58e44e09c87610737a249f8'}
            r = requests.get('https://api.football-data.org/v4/matches', headers=headers)
            return r.json() if r.status_code == 200 else None
        except:
            return None
    
    data = get_live()
    
    if data and 'matches' in data:
        comps = {}
        for m in data['matches']:
            c = m['competition']['name']
            if c not in comps: comps[c] = []
            comps[c].append(m)
        
        for comp, ms in comps.items():
            st.subheader(f"⚽ {comp}")
            for m in ms:
                home = m['homeTeam']['name']
                away = m['awayTeam']['name']
                status = m['status']
                
                if status in ['FINISHED', 'IN_PLAY', 'PAUSED']:
                    hg = m['score']['fullTime']['home'] or 0
                    ag = m['score']['fullTime']['away'] or 0
                    st.write(f"**{home}** {hg}-{ag} **{away}** ({status})")
                else:
                    kickoff = datetime.fromisoformat(m['utcDate'].replace('Z', '+00:00'))
                    st.write(f"{home} vs {away} (**{kickoff.strftime('%H:%M')}** - {status})")
            st.divider()
    else:
        st.warning("No live matches or API unavailable")

# ========== NEXT GAMES ==========
elif page == "📅 Next Games":
    st.title("📅 Upcoming Matches")
    st.caption(f"Next matches for {selected_league}")
    
    matches = get_upcoming_matches(selected_league)
    
    if matches:
        st.success(f"Found {len(matches)} upcoming matches")
        for m in matches[:15]:
            home = m['homeTeam']['name']
            away = m['awayTeam']['name']
            kickoff = datetime.fromisoformat(m['utcDate'].replace('Z', '+00:00'))
            
            # Try to get odds
            odds_str = ""
            if 'odds' in m and m['odds']:
                try:
                    odds = m['odds']['homeWin']
                    odds_str = f" | Odds: {odds}"
                except:
                    pass
            
            st.write(f"**{kickoff.strftime('%Y-%m-%d %H:%M')}** - {home} vs {away}{odds_str}")
    else:
        st.info("No upcoming matches found. The API might not have schedule data for this league.")

# ========== VALUE BETS ==========
elif page == "💎 Value Bets":
    st.title("💎 Value Bets")
    st.markdown("Find bets where odds are better than they should be")
    
    if 'B365H' in df.columns:
        dp = df.dropna(subset=['B365H', 'B365D', 'B365A']).copy()
        
        dp['Implied_H'] = dp['B365H'].apply(odds_to_prob)
        dp['Implied_D'] = dp['B365D'].apply(odds_to_prob)
        dp['Implied_A'] = dp['B365A'].apply(odds_to_prob)
        
        total = dp['Implied_H'] + dp['Implied_D'] + dp['Implied_A']
        dp['Implied_H'] = dp['Implied_H'] / total
        dp['Implied_D'] = dp['Implied_D'] / total
        dp['Implied_A'] = dp['Implied_A'] / total
        
        dp['Actual_H'] = (dp['FTR'] == 'H').astype(int)
        dp['Actual_D'] = (dp['FTR'] == 'D').astype(int)
        dp['Actual_A'] = (dp['FTR'] == 'A').astype(int)
        
        # Historical accuracy by odds bucket
        dp['Prob_Bucket'] = pd.cut(dp['Implied_H'], bins=[0, 0.2, 0.35, 0.5, 0.65, 0.8, 1.0], labels=['0-20%', '20-35%', '35-50%', '50-65%', '65-80%', '80-100%'])
        
        st.subheader("Historical Accuracy by Odds")
        acc_df = dp.groupby('Prob_Bucket')[['Actual_H', 'Actual_D', 'Actual_A']].mean().round(3)
        st.dataframe(acc_df)
        
        st.divider()
        
        # Find value
        recent = dp.sort_values('Date', ascending=False).head(50)
        value_bets = []
        
        for _, r in recent.iterrows():
            if r['Implied_H'] < 0.40 and r['Actual_H'] > 0.50:
                ev = (r['B365H'] * r['Actual_H']) - 1
                value_bets.append({'Match': f"{r['HomeTeam']} vs {r['AwayTeam']}", 'Bet': 'Home', 'Odds': r['B365H'], 'Implied': f"{r['Implied_H']*100:.1f}%", 'Actual': f"{r['Actual_H']*100:.1f}%", 'EV': f"{ev*100:.1f}%"})
            if r['Implied_A'] < 0.40 and r['Actual_A'] > 0.50:
                ev = (r['B365A'] * r['Actual_A']) - 1
                value_bets.append({'Match': f"{r['HomeTeam']} vs {r['AwayTeam']}", 'Bet': 'Away', 'Odds': r['B365A'], 'Implied': f"{r['Implied_A']*100:.1f}%", 'Actual': f"{r['Actual_A']*100:.1f}%", 'EV': f"{ev*100:.1f}%"})
        
        if value_bets:
            st.write(f"Found {len(value_bets)} potential value bets!")
            st.dataframe(pd.DataFrame(value_bets).head(10))
        else:
            st.info("No value bets found with current thresholds")
    else:
        st.warning("No odds data available")

# ========== ODDS COMPARISON ==========
elif page == "📊 Odds Comparison":
    st.title("📊 Odds Comparison")
    
    recent = df.sort_values('Date', ascending=False).head(20)
    bookmakers = ['B365', 'BF', 'BW', 'CL', 'LB', 'PS', 'Max']
    
    match_idx = st.selectbox("Select Match", range(len(recent)), 
                            format_func=lambda x: f"{recent.iloc[x]['HomeTeam']} vs {recent.iloc[x]['AwayTeam']}")
    
    match = recent.iloc[match_idx]
    
    st.subheader(f"{match['HomeTeam']} vs {match['AwayTeam']}")
    
    comparison = []
    for bm in bookmakers:
        h_col, d_col, a_col = f'{bm}H', f'{bm}D', f'{bm}A'
        if h_col in match.index and pd.notna(match[h_col]):
            comparison.append({'Bookmaker': bm, 'Home': match[h_col], 'Draw': match[d_col] if pd.notna(match[d_col]) else '-', 'Away': match[a_col] if pd.notna(match[a_col]) else '-'})
    
    comp_df = pd.DataFrame(comparison)
    if len(comp_df) > 0:
        st.dataframe(comp_df, use_container_width=True)
        
        st.divider()
        best_home = comp_df[comp_df['Home'] != '-']['Home'].astype(float).min()
        best_draw = comp_df[comp_df['Draw'] != '-']['Draw'].astype(float).min()
        best_away = comp_df[comp_df['Away'] != '-']['Away'].astype(float).min()
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Best Home", f"{best_home:.2f}")
        with col2: st.metric("Best Draw", f"{best_draw:.2f}")
        with col3: st.metric("Best Away", f"{best_away:.2f}")
    else:
        st.info("No odds data for this match")
