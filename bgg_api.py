import requests
from requests.adapters import HTTPAdapter, Retry
from io import StringIO

import pandas as pd
import xml.etree.ElementTree as ET

urls = {
    "collection": "https://boardgamegeek.com/xmlapi2/collection",
    "thing": "https://boardgamegeek.com/xmlapi2/thing"
}

def get_element_text(item, element):
    try:
        return item.find(element).text

    except:
        return None
    
        
def get_attribute_value(item, attribute):
    try:
        return item.find(attribute).attrib["value"]
    except:
        return None

s = requests.Session()

retries = Retry(total=10,
                backoff_factor=0.1,
                status_forcelist=[202, 500, 502, 503, 504 ])



payload = {
    'username':'DiceBoxPeterborough'
}

s.mount('https://', HTTPAdapter(max_retries=retries))

r = s.get(urls["collection"], params=payload)


df_collection = pd.read_xml(StringIO(r.text))
df_collection.drop_duplicates(subset="objectid", inplace=True)


thing_ids = df_collection["objectid"].unique()
thing_ids = list(map(str, thing_ids))

def get_things(ids: list) -> pd.DataFrame:
    payload = {
        'id': ",".join(ids)
    }
    r = s.get(urls["thing"], params=payload)
    xml = r.text

    data = []
    root = ET.fromstring(xml)

    print(xml)

    for item in root.findall('.//item'):   
        print(item.items())
        data.append({
            "id" : int(item.attrib['id']),
            "type" : item.attrib["type"],
            "thumbnail" : get_element_text(item, "thumbnail"),
            "image" : get_element_text(item, "image"),
            "description" : get_element_text(item, "description"),
            "year_published" : get_element_text(item, "yearpublished"),
            "min_players" : get_attribute_value(item, "minplayers"),
            "max_players" : get_attribute_value(item, "maxplayers"),
            "playing_time" : get_attribute_value(item, "playingtime"),
            "min_playtime" : get_attribute_value(item, "minplaytime")
        })
        exit()

    df = pd.DataFrame(data)
    return df


df_things = get_things(thing_ids)

    
df = pd.merge(left=df_collection, right=df_things, left_on="objectid", right_on="id", validate="m:1")
df.to_csv('bgg_export.csv')