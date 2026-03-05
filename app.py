"""
SoccerStats - Premium Football Analytics Dashboard
v2.1 - Refactored with caching, error handling, and modular structure
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
    initial_sidebar_state="expanded"
)

# Premium CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Outfit', sans-serif !important; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Space Grotesk', sans-serif !important; }
    
    .stApp { background: #0a0a0f; color: #e0e0e0; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
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
    }
    
    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 42px;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 50%, #ff006e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label { color: #888; font-size: 13px; text-transform: uppercase; letter-spacing: 2px; margin-top: 8px; }
    
    /* Footer fix */
    .footer { text-align: center; color: #666; padding: 20px; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)


def main():
    st.markdown("# ⚽ SoccerStats Pro")
    st.markdown("### Premium Football Analytics")
    
    # Sidebar - League & Season Selection
    with st.sidebar:
        st.markdown("## Select League")
        league = st.selectbox("League", list(LEAGUE_URLS.keys()), index=0)
        
        st.markdown("## Select Season")
        seasons = get_available_seasons(league)
        season = st.selectbox("Season", seasons, index=len(seasons)-1)
        
        st.markdown("---")
        st.caption(f"Data by football-data.co.uk")
    
    # Load data with loading indicator
    with st.spinner(f"Loading {league} {season} data..."):
        df = load_match_data(league, season)
    
    # Error handling
    if df.empty:
        st.error(f"No data available for {league} {season}. Please try a different selection.")
        return
    
    # Show data info
    st.success(f"Loaded {len(df)} matches")
    
    # Calculate stats
    team_stats = get_team_stats(df)
    
    if team_stats.empty:
        st.error("Unable to calculate team statistics. Data format may have changed.")
        return
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 League Table", "📈 Stats", "🎯 Form Guide", "🔢 Betting Stats", "⚖️ Compare"])
    
    # === TAB 1: League Table ===
    with tab1:
        st.markdown("### League Table")
        
        for idx, row in team_stats.iterrows():
            pos = idx + 1
            medal = format_position(pos)
            st.markdown(f"""
                <div class="glass-card" style="display:flex; align-items:center; padding:16px 24px;">
                    <span style="font-size:20px; width:40px;">{medal}</span>
                    <span style="flex:1; font-weight:600; font-size:16px;">{row['Team']}</span>
                    <span style="color:#888; margin-right:20px;">{row['P']}</span>
                    <span style="color:#00d4ff; width:50px; text-align:center;">{row['W']}</span>
                    <span style="color:#7b2cbf; width:50px; text-align:center;">{row['D']}</span>
                    <span style="color:#ff006e; width:50px; text-align:center;">{row['L']}</span>
                    <span style="color:#00d4ff; width:50px; text-align:center; font-weight:600;">{row['Pts']}</span>
                </div>
            """, unsafe_allow_html=True)
    
    # === TAB 2: Stats ===
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Top Scorers")
            top = team_stats.nlargest(10, 'GF')[['Team', 'GF']].iloc[::-1]
            fig1 = px.bar(top, x='GF', y='Team', orientation='h', color='GF', color_continuous_scale='Greens')
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font={'color': '#888'}, showlegend=False, height=400, margin=dict(t=20, b=20, l=150, r=20))
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown("#### 🛡️ Best Defense")
            best = team_stats.nsmallest(10, 'GA')[['Team', 'GA']].iloc[::-1]
            fig2 = px.bar(best, x='GA', y='Team', orientation='h', color='GA', color_continuous_scale='Blues')
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font={'color': '#888'}, showlegend=False, height=400, margin=dict(t=20, b=20, l=150, r=20))
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("#### 📊 Goal Difference")
        gd = team_stats.sort_values('GD')[['Team', 'GD']]
        fig3 = px.bar(gd, x='GD', y='Team', orientation='h', color='GD', color_continuous_scale=[[0, '#ff006e'], [0.5, '#1a1a2e'], [1, '#00d4ff']])
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font={'color': '#888'}, showlegend=False, height=500, margin=dict(t=20, b=20, l=150, r=20))
        st.plotly_chart(fig3, use_container_width=True)
    
    # === TAB 3: Form Guide ===
    with tab3:
        st.markdown("#### 🎯 Team Form Guide")
        selected_team = st.selectbox("Select Team", team_stats['Team'].tolist())
        
        form = calculate_form_guide(df, selected_team)
        
        if form:
            cols = st.columns(len(form))
            for i, (col, result) in enumerate(zip(cols, form)):
                color = get_form_color(result)
                col.markdown(f"""
                    <div style="background:{color}; color:#000; padding:12px; border-radius:8px; text-align:center; font-weight:700;">
                        {result}
                    </div>
                """, unsafe_allow_html=True)
        
        # Show last 5 matches details
        home = df[df['HomeTeam'] == selected_team].copy()
        away = df[df['AwayTeam'] == selected_team].copy()
        home['Result'] = home['FTR'].apply(lambda x: 'H' in x)
        away['Result'] = away['FTR'].apply(lambda x: 'A' in x)
        
        st.markdown("#### Recent Matches")
        recent = pd.concat([home, away]).tail(5)
        if not recent.empty:
            for _, match in recent.iterrows():
                st.markdown(f"**{match['HomeTeam']}** {match['FTHG']}-{match['FTAG']} **{match['AwayTeam']}**")
    
    # === TAB 4: Betting Stats ===
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Over/Under 2.5 Goals")
            ou = calculate_over_under(df)
            st.markdown(f"""
                <div class="glass-card">
                    <div class="metric-value">{ou['over_pct']}%</div>
                    <div class="metric-label">Over 2.5 ({ou['over']} matches)</div>
                </div>
                <div class="glass-card">
                    <div class="metric-value">{100 - ou['over_pct']}%</div>
                    <div class="metric-label">Under 2.5 ({ou['under']} matches)</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Both Teams To Score")
            btts = calculate_btts(df)
            st.markdown(f"""
                <div class="glass-card">
                    <div class="metric-value">{btts['yes_pct']}%</div>
                    <div class="metric-label">BTTS Yes ({btts['yes']} matches)</div>
                </div>
                <div class="glass-card">
                    <div class="metric-value">{btts['no']}%</div>
                    <div class="metric-label">BTTS No ({btts['no']} matches)</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("#### Most Common Scorelines")
        scores = get_scoreline_counts(df)
        for score, count in scores.items():
            st.markdown(f"**{score}**: {count} matches")
    
    # === TAB 5: Compare ===
    with tab5:
        st.markdown("#### ⚖️ Team Comparison")
        teams = st.multiselect("Select teams", team_stats['Team'].tolist(), default=team_stats['Team'].tolist()[:3])
        
        if teams:
            comp = team_stats[team_stats['Team'].isin(teams)]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Wins', x=comp['Team'], y=comp['W'], marker_color='#00d4ff'))
            fig.add_trace(go.Bar(name='Draws', x=comp['Team'], y=comp['D'], marker_color='#7b2cbf'))
            fig.add_trace(go.Bar(name='Losses', x=comp['Team'], y=comp['L'], marker_color='#ff006e'))
            
            fig.update_layout(barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font={'color': '#888'}, height=400, legend=dict(orientation='h', y=1.1, x=0.5, xanchor='center'))
            st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown('<div class="footer">SoccerStats Pro v2.1 · Built with Streamlit · Data by football-data.co.uk</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
