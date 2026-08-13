import streamlit as st
from helpers.getPlayerData import playerList
import pandas as pd
st.set_page_config(page_title="SoccerHotzone", page_icon=":soccer:")
st.title("SoccerHotzone")
players=[player["name"] for player in playerList]
print(players)
st.selectbox("Select a player", players, key="selected_player", help="Select a player to view their shot data.", index=0)
