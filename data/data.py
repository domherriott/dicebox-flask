import pandas as pd
import io
import requests
import os
from pathlib import Path

url = 'https://bgg-json.azurewebsites.net/collection/edwalter'

x = requests.get(url=url).content 
df = pd.read_json(io.StringIO(x.decode('utf8')))

df = df[[
    "gameId",
    "name",
    "image",
    "thumbnail",
    "minPlayers",
    "maxPlayers",
    "isExpansion",
    "yearPublished"
]]

print(df.columns)
print(df.head())

cwd = Path(os.path.dirname(os.path.abspath(__file__)))

df.to_csv(cwd / 'data.csv')