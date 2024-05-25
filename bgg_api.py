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
    
def process_links(item, link_type):
    info = []
    try:
        links = item.findall('.//link')
        for link in links:
            if link.attrib["type"] == link_type:
                info.append(link.attrib["value"])
        return info
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
    print(xml)
    data = []
    root = ET.fromstring(xml)


    categories = []
    mechanics = []

    for item in root.findall('.//item'):   
    
        print(item)

        id = int(item.attrib['id']) 


        data.append({
            "id" : id,
            "type" : item.attrib["type"],
            "thumbnail" : get_element_text(item, "thumbnail"),
            "image" : get_element_text(item, "image"),
            "description" : get_element_text(item, "description"),
            "year_published" : get_element_text(item, "yearpublished"),
            "min_players" : get_attribute_value(item, "minplayers"),
            "max_players" : get_attribute_value(item, "maxplayers"),
            "playing_time" : get_attribute_value(item, "playingtime"),
            "min_playtime" : get_attribute_value(item, "minplaytime"),
        })

        for cat in process_links(item=item, link_type="boardgamecategory"):
            categories.append({
                "id" : id,
                "category" : cat
            })

        for mech in process_links(item=item, link_type="boardgamemechanic"):
            mechanics.append({
                "id" : id,
                "mechanic" : mech
            })

 

    df_things = pd.DataFrame(data)
    df_cat = pd.DataFrame(categories)
    df_mech = pd.DataFrame(mechanics)
    return df_things, df_cat, df_mech


df_things, df_cat, df_mech  = get_things(thing_ids)

    
df = pd.merge(left=df_collection, right=df_things, left_on="objectid", right_on="id", validate="m:1")


print(df)
df.to_csv('bgg_export.csv')


df_cat_mapping = pd.read_csv('./reference_data/category_mapping.csv')
print(df_cat_mapping)

df_cat = pd.merge(left=df_cat, right=df_cat_mapping, left_on="category", right_on="category", validate="m:1")
df_cat = df_cat[['id', 'high_level_category']].drop_duplicates()
print(df_cat)

df_mech_mapping = pd.read_csv('./reference_data/mechanic_mapping.csv')
print(df_mech_mapping)

df_mech = pd.merge(left=df_mech, right=df_mech_mapping, left_on="mechanic", right_on="mechanic", validate="m:1")
df_mech = df_mech[['id', 'high_level_mechanic']].drop_duplicates()

df_cat.to_csv('bgg_export_cat.csv')
df_mech.to_csv('bgg_export_mech.csv')