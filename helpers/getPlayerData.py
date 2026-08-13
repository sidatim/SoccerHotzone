import requests
import json
import time
import pprint as pp
playerList=[
    {
        "name": "Lionel Messi",
        "position": "Forward",
        "preferred_foot": "Left",
        "understat_id": 2097
    },
    {
        "name": "Cristiano Ronaldo",
        "position": "Forward",
        "preferred_foot": "Right",
        "understat_id": 2371
    },
    {
        "name": "Kylian Mbappé",
        "position": "Forward",
        "preferred_foot": "Right",
        "understat_id": 3423
    },
    {
        "name": "Erling Haaland",
        "position": "Forward",
        "preferred_foot": "Left",
        "understat_id": 8260
    },
    {
        "name": "Robert Lewandowski",
        "position": "Forward",
        "preferred_foot": "Right",
        "understat_id": 227
    },
    {
        "name": "Harry Kane",
        "position": "Forward",
        "preferred_foot": "Right",
        "understat_id": 647
    },
    {
        "name": "Mohamed Salah",
        "position": "Forward",
        "preferred_foot": "Left",
        "understat_id": 1250
    },
    {
        "name": "Lautaro Martinez",
        "position": "Forward",
        "preferred_foot": "Right",
        "understat_id": 7006
    },
    {
        "name": "Romelu Lukaku",
        "position": "Forward",
        "preferred_foot": "Left",
        "understat_id": 594
    },
    {
        "name": "Karim Benzema",
        "position": "Forward",
        "preferred_foot": "Right",
        "understat_id": 2370
    },
    {
        "name": "Pierre-Emerick Aubameyang",
        "position": "Forward",
        "preferred_foot": "Right",
        "understat_id": 318
    }
]

if __name__== "__main__":
    for player in playerList:
        understat_id=player["understat_id"]
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
            with open(f"getData/{player['name']}.json", "w", encoding="utf-8") as f:
                json.dump(getPlayerData.json(), f, indent=4)
        else:
            pp.pprint(f"Failed to retrieve data for {player['name']}. Status code: {getPlayerData.status_code} Response: {getPlayerData.text}")
        time.sleep(1)
