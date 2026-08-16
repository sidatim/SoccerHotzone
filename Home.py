import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mplsoccer as mp
from plotShots import plotGoals, BODY_PART_FILTERS, SHOT_TYPE_FILTERS
import json


st.set_page_config(
    page_title="SoccerHotzone", 
    page_icon=":soccer:",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1em;
        font-weight: 600;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .header-text {
        font-size: 2.5em;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5em;
    }
    .subtitle-text {
        font-size: 1.2em;
        color: #666;
        margin-bottom: 2em;
    }
    .filter-section {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)


with open("helpers/players.json", "r", encoding="utf-8") as f:
    playerList=json.load(f)["players"]


col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 class="header-text">⚽ SoccerHotzone</h1>', unsafe_allow_html=True)
with col2:
    st.markdown("", unsafe_allow_html=True)

st.markdown('<p class="subtitle-text">Explore where top soccer players score and discover their shooting hot zones</p>', unsafe_allow_html=True)

players=[player["name"] for player in playerList]


with st.sidebar:
    st.header("🎯 Player Selection")
    selectedPlayer = st.selectbox(
        "Select a player", 
        players, 
        key="selected_player", 
        help="Select a player to view their shot data.",
        index=None
    )

if selectedPlayer:
    with open(f"shotData/{selectedPlayer}_shots.json", "r", encoding="utf-8") as f:
        player_shots = json.load(f)
    
    available_seasons = sorted({int(shot["season"]) for shot in player_shots})
    season_options = ["All seasons"] + [
        f"{year}/{str(year + 1)[-2:]}" for year in available_seasons
    ]
    
    if st.session_state.get("selected_season") not in season_options:
        st.session_state["selected_season"] = "All seasons"
    
    with st.sidebar:
        st.divider()
        st.header("📅 Season")
        selected_season = st.selectbox(
            "Select a season (optional)", 
            season_options, 
            key="selected_season",
            help="Only seasons with data for the selected player are listed.",
        )

with st.sidebar:
    st.divider()
    st.header("🔍 Filters")
    shotFilters = st.multiselect(
        "Shot type filters (optional)", 
        default=None, 
        options=SHOT_TYPE_FILTERS,
        help="Filter shots by type"
    )
    bodyParts = st.multiselect(
        "Body part filters (optional)", 
        default=None, 
        options=BODY_PART_FILTERS,
        help="Filter shots by body part used"
    )

if selectedPlayer and (shotFilters or bodyParts):
    playerData=next((player for player in playerList if player["name"]==selectedPlayer), None)
    season_year = None if selected_season == "All seasons" else selected_season[:4]
    
    scatterFig, scatterAx, heatmapFig, heatmapAx, stats=plotGoals(playerData, shotFilters, bodyParts, season_year)
    statdf=pd.DataFrame.from_dict(stats, orient="index", columns=["Statistics"])

    tab1, tab2, tab3 = st.tabs(["📊 Shot Map", "🔥 Heat Zone", "🎯 Combined View"])
    
    with tab1:
        st.subheader(f"{selectedPlayer} - Shot Map")
        st.pyplot(scatterFig, width="stretch")
    
    with tab2:
        st.subheader(f"{selectedPlayer} - Heat Zone")
        st.pyplot(heatmapFig, width="stretch")
    
    with tab3:
        st.subheader(f"{selectedPlayer} - Combined Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(scatterFig, width="stretch")
        with col2:
            st.pyplot(heatmapFig, width="stretch")
            
    st.divider()
    st.subheader("📋 Detailed Statistics")
    st.dataframe(statdf, width="stretch", hide_index=False)

elif selectedPlayer and not (shotFilters or bodyParts):
    st.warning("⚠️ Please select at least one filter to view the analysis", icon="⚠️")