import mplsoccer as mp
import json
import pandas as pd
import timeit
import streamlit as st
st.cache_data(show_spinner=False,  ttl=None)
def plotGoals(playerName):
    start_time=timeit.default_timer()
    with open(f"shotData/{playerName}_shots.json", "r", encoding="utf-8") as f:
        shotData=json.load(f)
    shotData=pd.DataFrame(shotData)
    goals=shotData[shotData["result"]=="Goal"]
    if goals.empty:
        st.warning(f"No goals found for {playerName}")
        st.stop()
    pitch=mp.VerticalPitch(pitch_type='metricasports', pitch_width=105, pitch_length=100, pad_bottom=0.01, pitch_color='#22312b', line_color='#c7d5cc',  goal_type='box',stripe_color='#c7d5cc', half=True)
    fig, ax=pitch.draw()
    ax.scatter(goals["X"]*105, goals["Y"]*100, s=100, c="red", edgecolors="black", alpha=0.7)
    return fig, ax 