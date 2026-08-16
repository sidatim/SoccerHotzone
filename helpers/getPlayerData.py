import requests
import json
import time
import pprint as pp
import os

if __name__== "__main__":
    
    with open("helpers/players.json", "r", encoding="utf-8") as f:
        playerList=json.load(f)["players"]
    for player in playerList:
        understat_id=player["understat_id"]
        if os.path.exists(f"shotData/{player['name']}_shots.json"):
            print(f"Data for {player['name']} already exists. Skipping retrieval.")
            continue
        url=f"https://understat.com/getPlayerData/{understat_id}"
        headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"https://understat.com/player/{understat_id}",
            }
        getPlayerData=requests.get(url, headers=headers)
        if getPlayerData.status_code==200:
            print(f"Data for {player['name']} retrieved successfully.")
            shotData=getPlayerData.json()["shots"]
            if shotData:
                with open(f"shotData/{player['name']}_shots.json", "w", encoding="utf-8") as f:
                    json.dump(shotData, f, indent=4)
                print(f"Shot data for {player['name']} saved to shotData/{player['name']}_shots.json")            
        else:
            pp.pprint(f"Failed to retrieve data for {player['name']}. Status code: {getPlayerData.status_code} Response: {getPlayerData.text}")
        time.sleep(1)
