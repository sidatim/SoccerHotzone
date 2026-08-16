import mplsoccer as mp
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


SHOT_TYPE_FILTERS = [
    "Goals",
    "Shots on Target",
    "Non-Penalty Goals",
    "All Shots",
    ]
BODY_PART_FILTERS=[
    "Preferred Foot",
    "Weak Foot",
    "Headers",
    "Other Body Part"
]



@st.cache_data(show_spinner=False, ttl=None)
def filter_events(events, shotFilters, bodyFilters, preferred_foot, season=None):
    if not shotFilters and not bodyFilters:
        filtered = events.copy()
        stats=calculateStatistics(filtered)
    else:
        filtered = events.copy()
        selected = set(shotFilters).union(set(bodyFilters))

        result_filters = selected.intersection(
            {"Goals", "Shots on Target", "Non-Penalty Goals", "All Shots"}
        )
        if result_filters and "All Shots" not in result_filters:
            result_mask = pd.Series(False, index=filtered.index)
            if "Goals" in result_filters:
                result_mask |= filtered["result"].eq("Goal")
            if "Shots on Target" in result_filters:
                result_mask |= filtered["result"].isin(["Goal", "SavedShot"])
            if "Non-Penalty Goals" in result_filters:
                result_mask |= (
                    filtered["result"].eq("Goal")
                    & filtered["situation"].ne("Penalty")
                )
            filtered = filtered.loc[result_mask]
        body_part_filters=selected.intersection({"Preferred Foot", "Weak Foot", "Headers", "Other Body Part"})
        
        if body_part_filters:
            allowed_shot_types = set()
            preferred_shot_type = f"{preferred_foot.title()}Foot"
            weak_shot_type = "RightFoot" if preferred_shot_type == "LeftFoot" else "LeftFoot"
            if "Preferred Foot" in body_part_filters:
                allowed_shot_types.add(preferred_shot_type)
            if "Weak Foot" in body_part_filters:
                allowed_shot_types.add(weak_shot_type)
            if "Headers" in body_part_filters:
                allowed_shot_types.add("Head")
            filtered = filtered.loc[filtered["shotType"].isin(allowed_shot_types)]
    if season is not None:
        filtered = filtered.loc[filtered["season"].astype(str).eq(str(season))]
    return filtered


@st.cache_data(show_spinner=False, ttl=None)
def plotGoals(player, shotFilters, bodyFilters, season=None):
    with open(f"shotData/{player['name']}_shots.json", "r", encoding="utf-8") as f:
        shotData=json.load(f)
    shotData=pd.DataFrame(shotData)
    shotData["X"] = shotData["X"].astype(float) 
    shotData["Y"] = shotData["Y"].astype(float)
    events = filter_events(shotData, shotFilters, bodyFilters, player["preferred_foot"], season)
    if events.empty:
        st.warning(f"No shots found for {player['name']} with the selected filters")
        st.stop()

    pitch=mp.VerticalPitch(pitch_type='metricasports', pitch_width=68, pitch_length=100, pad_bottom=0.01, pitch_color='#22312b', line_color='#c7d5cc',  goal_type='box',stripe_color='#c7d5cc', half=True, axis=True)
    heatmapPitch=mp.VerticalPitch(pitch_type='metricasports', pitch_width=68, pitch_length=100, pad_bottom=0.01, pitch_color='#22312b', line_color='#c7d5cc',  goal_type='box',stripe_color='#c7d5cc', half=True, axis=True)
    scatterFig, scatterAx=pitch.draw(figsize=(10,6))
    heatmapFig, heatmapAx=pitch.draw(figsize=(10,6))
    x_plot = events["X"]
    y_plot = 1 - events["Y"]
    goal_events = events[events["result"] == "Goal"]
    non_goal_events = events[events["result"] != "Goal"]
    if not non_goal_events.empty:
        pitch.scatter(
            x=non_goal_events["X"], y=1 - non_goal_events["Y"], s=20,
            c="#74b9ff", edgecolors="black", alpha=0.7, ax=scatterAx,
            label="Other shots",
        )
    if not goal_events.empty:
        pitch.scatter(
            x=goal_events["X"], y=1 - goal_events["Y"], s=20,
            c="red", edgecolors="black", alpha=0.7, ax=scatterAx,
            label="Goals",
        )
    if not goal_events.empty and not non_goal_events.empty:
        scatterAx.legend(loc="upper right")

    bin_statistic=heatmapPitch.bin_statistic(x=x_plot, y=y_plot, bins=(20, 10), statistic='count', normalize=True, )
    hm = heatmapPitch.heatmap(bin_statistic, cmap='Reds', edgecolors='#22312b', ax=heatmapAx, alpha=0.7)
   
    cbar = plt.colorbar(hm, ax=heatmapAx, label='Frequency (% of Shots)')
    labels=heatmapPitch.label_heatmap(bin_statistic, color='#22312b', fontsize=14, ax=heatmapAx, ha='center', va='center', str_format='{:.0%}', )
    stats=calculateStatistics(events, shotFilters, bodyFilters)
    """
    maxZone=getMaxZone(labels, bin_statistic, x_plot, y_plot)
    if maxZone[1] is not None:
        max_label = maxZone[1]
        pos = max_label.get_position()
        circle = Circle((pos[0], pos[1]), radius=0.03, linewidth=3, edgecolor='yellow', facecolor='none', zorder=10)
        heatmapAx.add_patch(circle)
    """
    
    return scatterFig, scatterAx, heatmapFig, heatmapAx, stats


def calculateStatistics(events, shotFilters, bodyFilters):
    total_shots=len(events)
    total_goals=len(events[events["result"]=="Goal"])
    shotAccuracy=total_goals/total_shots if total_shots>0 else 0
    events["xG"]=events["xG"].astype(float)
    total_xG=events["xG"].sum()
    xG_difference=total_goals-total_xG
    xG_perShot=total_xG/total_shots if total_shots>0 else 0
    if shotFilters:
        if (("Goals" in shotFilters) or ("Non-Penalty Goals" in shotFilters)) and (("Shots on Target" not in shotFilters) or ("All Shots" not in shotFilters)):
          return{
              "Total Shots": total_shots,
              "Total Goals": total_goals,
                "Total xG": total_xG,
                "Goals-xG": xG_difference,
                "xG per Goal": xG_perShot
          }
    return{
        "Total Shots": total_shots,
        "Total Goals": total_goals,
        "Shot Accuracy": f"{shotAccuracy:.1%}",
        "Total xG": total_xG,
        "Goals-xG": xG_difference,
        "xG per Shot": xG_perShot
    }
"""
def getMaxZone(labels, bin_statistic, x_plot, y_plot):
    max_value = -1
    max_label = None
    max_idx = None
    for i, label in enumerate(labels):
        try:
            value = int(label.get_text().strip('%')) / 100
            if value > max_value:
                max_value = value
                max_label = label
                max_idx = i
        except ValueError:
            continue
    
    if max_label and max_value > 0:
        tied_indices = []
        for i, label in enumerate(labels):
            try:
                value = int(label.get_text().strip('%')) / 100
                if value == max_value:
                    tied_indices.append(i)
            except ValueError:
                continue
        
        if len(tied_indices) > 1:
            bins_x, bins_y = 20, 10  
            max_x = -1
            best_idx = tied_indices[0]
            for idx in tied_indices:
                label_pos = max_label.get_position() if idx == tied_indices[0] else label.get_position()
                if label_pos[0] > max_x:  
                    max_x = label_pos[0]
                    best_idx = idx
                    max_label = label
            max_idx = best_idx   
    return max_value, max_label, max_idx
    """