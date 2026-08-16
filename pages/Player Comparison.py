import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mplsoccer as mp
from plotShots import plotGoals, SHOT_TYPE_FILTERS
import json

BODY_PARTS=[
    "Preferred Foot",
    "Weak Foot",
    "Headers"
]
if "show_scatter" not in st.session_state:
    st.session_state["show_scatter"] = False
with open("helpers/players.json", "r", encoding="utf-8") as f:
    playerList=json.load(f)["players"]
st.set_page_config(page_title="Player Comparison", page_icon=":soccer:")
st.title("Player Comparison")
players=[player["name"] for player in playerList]
st.text("Compare the shot locations of two soccer players to see how they differ in their scoring patterns. This app allows you to visualize and analyze the shot data of top soccer players side by side.")
col1, col2 = st.columns(2)  
with col1:
    selectedPlayer1=st.selectbox("Select Player 1", players, key="selected_player_1", help="Select the first player to compare.", index=None)
with col2:
    selectedPlayer2=st.selectbox("Select Player 2", options=[player['name'] for player in playerList if player['name']!=selectedPlayer1], key="selected_player_2", help="Select the second player to compare.", index=None, )

shotTypes=st.multiselect("Select shot type filters", default=None, options=SHOT_TYPE_FILTERS)
bodyParts=st.multiselect("Select body part filters", default=None, options=BODY_PARTS)
show_scatter=st.checkbox("Show Scatter Plots", value=False, key="show_scatter", help="Check to display scatter plots for both players.")
    
if (shotTypes or bodyParts) and selectedPlayer1 and selectedPlayer2:
    playerData1=next((player for player in playerList if player["name"]==selectedPlayer1), None)
    playerData2=next((player for player in playerList if player["name"]==selectedPlayer2), None)
    scatterFig1, scatterAx1, heatmapFig1, heatmapAx1, stats1=plotGoals(playerData1, shotTypes, bodyParts)
    scatterFig2, scatterAx2, heatmapFig2, heatmapAx2, stats2=plotGoals(playerData2, shotTypes, bodyParts)
    col3, col4 = st.columns(2)
    statsdf1=pd.DataFrame.from_dict(stats1, orient="index", columns=["Statistics"])
    statsdf2=pd.DataFrame.from_dict(stats2, orient="index", columns=["Statistics"])
    if show_scatter:
        with col3:
            st.text(f"{selectedPlayer1} Scatter Plot")
            st.pyplot(scatterFig1, width="stretch")
            st.dataframe(statsdf1, width="stretch",selection_mode="single-row", on_select="ignore")
        with col4:
            st.text(f"{selectedPlayer2} Scatter Plot")
            st.pyplot(scatterFig2, width="stretch")
            st.dataframe(statsdf2, width="stretch",selection_mode="single-row", on_select="ignore")
    else:
        with col3:
            st.text(f"{selectedPlayer1} Heatmap")
            st.pyplot(heatmapFig1, width="stretch")
            st.dataframe(statsdf1, width="stretch",selection_mode="single-row", on_select="ignore")
        with col4:
            st.text(f"{selectedPlayer2} Heatmap")
            st.pyplot(heatmapFig2, width="stretch")
            st.dataframe(statsdf2, width="stretch",selection_mode="single-row", on_select="ignore", )
        
  
    