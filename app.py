import streamlit as st
from helpers.getPlayerData import playerList
import pandas as pd
import matplotlib.pyplot as plt
import mplsoccer as mp
from plotShots import plotGoals
st.set_page_config(page_title="SoccerHotzone", page_icon=":soccer:")
st.title("SoccerHotzone")
players=[player["name"] for player in playerList]
selectedPlayer=st.selectbox("Select a player", players, key="selected_player", help="Select a player to view their shot data.", index=None)
print(selectedPlayer)
st.pyplot(fig)
if selectedPlayer:
    fig, ax=plotGoals(selectedPlayer)
    st.pyplot(ax.figure)