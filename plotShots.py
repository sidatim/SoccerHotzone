import mplsoccer as mp
import json
import pandas as pd
import streamlit as st
st.cache_data(show_spinner=False,  ttl=None)
def plotGoals(playerName):
    with open(f"shotData/{playerName}_shots.json", "r", encoding="utf-8") as f:
        shotData=json.load(f)
    shotData=pd.DataFrame(shotData)
    shotData["X"] = shotData["X"].astype(float) 
    shotData["Y"] = shotData["Y"].astype(float)
    goals=shotData[shotData["result"]=="Goal"]
    if goals.empty:
        st.warning(f"No goals found for {playerName}")
        st.stop()
    pitch=mp.VerticalPitch(pitch_type='metricasports', pitch_width=68, pitch_length=100, pad_bottom=0.01, pitch_color='#22312b', line_color='#c7d5cc',  goal_type='box',stripe_color='#c7d5cc', half=True, axis=True)
    fig, ax=pitch.draw(figsize=(10,6))
    x_plot = goals["X"]
    y_plot = 1 - goals["Y"]
    pitch.scatter(x=x_plot, y=y_plot, s=20, c="red", edgecolors="black", alpha=0.7, ax=ax)
    return fig, ax 