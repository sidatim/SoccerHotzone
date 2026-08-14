import mplsoccer as mp
import json
import pandas as pd
import streamlit as st
st.cache_data(show_spinner=False,  ttl=None)
def plotGoals(player, filters):
    with open(f"shotData/{player['name']}_shots.json", "r", encoding="utf-8") as f:
        shotData=json.load(f)
    shotData=pd.DataFrame(shotData)
    shotData["X"] = shotData["X"].astype(float) 
    shotData["Y"] = shotData["Y"].astype(float)
    goals=shotData[shotData["result"]=="Goal"]
    if goals.empty:
        st.warning(f"No goals found for {player['name']}")
        st.stop()

    pitch=mp.VerticalPitch(pitch_type='metricasports', pitch_width=68, pitch_length=100, pad_bottom=0.01, pitch_color='#22312b', line_color='#c7d5cc',  goal_type='box',stripe_color='#c7d5cc', half=True, axis=True)
    heatmapPitch=mp.VerticalPitch(pitch_type='metricasports', pitch_width=68, pitch_length=100, pad_bottom=0.01, pitch_color='#22312b', line_color='#c7d5cc',  goal_type='box',stripe_color='#c7d5cc', half=True, axis=True)
    scatterFig, scatterAx=pitch.draw(figsize=(10,6))
    heatmapFig, heatmapAx=pitch.draw(figsize=(10,6))
    x_plot = goals["X"]
    y_plot = 1 - goals["Y"]
    pitch.scatter(x=x_plot, y=y_plot, s=20, c="red", edgecolors="black", alpha=0.7, ax=scatterAx)
    bin_statistic=heatmapPitch.bin_statistic(x=x_plot, y=y_plot, bins=(20, 10), statistic='count', normalize=True, )
    heatmapPitch.heatmap(bin_statistic, cmap='Reds', edgecolors='#22312b', ax=heatmapAx, alpha=0.5)
    labels=heatmapPitch.label_heatmap(bin_statistic, color='#22312b', fontsize=14, ax=heatmapAx, ha='center', va='center', str_format='{:.0%}', )
    return scatterFig, scatterAx, heatmapFig, heatmapAx