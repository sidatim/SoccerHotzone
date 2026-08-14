import streamlit as st
from helpers.getPlayerData import playerList
import pandas as pd
import matplotlib.pyplot as plt
import mplsoccer as mp
from plotShots import plotGoals
st.set_page_config(page_title="SoccerHotzone", page_icon=":soccer:")
st.title("SoccerHotzone")
players=[player["name"] for player in playerList]
st.text("Ever wondered where your favorite soccer player scores their goals from? This app allows you to visualize the shot locations of top soccer players to see where they are most effective on the pitch.")
selectedPlayer=st.selectbox("Select a player", players, key="selected_player", help="Select a player to view their shot data.", index=None)
seasons=[f"{year}-{year+1}" for year in range(2010, 2025)]
season=st.selectbox("Select a season", seasons, key="selected_season", help="Select a season to view the player's shot data.", index=None)
filters=st.multiselect("Select filters", default=["Goals"], options=["Goals", "Shots on Target", "Non-Penalty Goals", "All Shots", "Preferred Foot", "Weak Foot"])
if selectedPlayer:
    playerData=next((player for player in playerList if player["name"]==selectedPlayer), None)
    scatterFig, scatterAx, heatmapFig, heatmapAx=plotGoals(playerData, filters)
    st.pyplot(scatterFig)
    st.pyplot(heatmapAx.get_figure())