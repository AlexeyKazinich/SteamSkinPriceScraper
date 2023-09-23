import requests
import json
from enum import Enum
import re
from urllib.parse import unquote, quote

#use regex expressions to clean up the market_name for the MarketplaceItem: Gun: .... Skin .... Quality .... Stattrak T/F

# Goal for this project
# - fill out an excel sheet or google sheet with gun names and the price I paid for each item
# - use this code to find the current prices for all those items
# - count how much I'm profiting assuming a 20% market cut when sold
# - draw a graph of my asset value
#


marketplace_items = {}

class AppID(Enum):
    csgo = "730"
    tf2 = "440"
    
class MarketName(Enum):
    FT_AK_REDLINE = "AK-47%20%7C%20Redline%20%28Field-Tested%29"
    ST_FT_AK_REDLINE = "StatTrak™%20AK-47%20%7C%20Redline%20%28Field-Tested%29"

class MarketPlaceItem:
    def __init__(self,name = str, lowest_price = str, volume = str, median_price = str, wear = str, statTrak = bool):
        self.name = name
        self.volume = volume
        self.lowest_price = lowest_price
        self.median_price = median_price
        self.wear = wear
        self.statTrak = statTrak
    
    def print_self(self):
        if self.statTrak:
            print(f"name: StatTrak {self.name} || wear: {self.wear} || price: {self.lowest_price}")
        else:
            print(f"name: {self.name} || wear: {self.wear} || price: {self.lowest_price}")

class Currency(Enum):
    USD = "1"
    CAD = "20"
    

def get_item_info(app_id: str,market_name: str, currency : str):
    url = f"https://steamcommunity.com/market/priceoverview/?appid={app_id}&market_hash_name={market_name}&currency={currency}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        
        if 'success' in data and data['success']:
            x = unquote(market_name)
            statTrak = False
            if re.search("StatTrak", x):
                x = x[10:]
                statTrak = True
                
            gun_name = re.search("^(.*?)\s\(",x).group(1)          
            wear = re.search("\((.*?)\)", x).group(1)
            
            if statTrak:
                marketplace_items[f"{gun_name} StatTrak"] = MarketPlaceItem(gun_name,data["lowest_price"],data["volume"],data["median_price"],wear,True)
            else:
                marketplace_items[f"{gun_name}"] = MarketPlaceItem(gun_name,data["lowest_price"],data["volume"],data["median_price"],wear,False)
            
        else:
            print ("Failed to fetch data")
    
    else:
        print(f"HTTP Error {response.status_code}")

get_item_info(AppID.csgo.value,MarketName.ST_FT_AK_REDLINE.value,Currency.CAD.value)
get_item_info(AppID.csgo.value,MarketName.FT_AK_REDLINE.value,Currency.CAD.value)


for key, value in marketplace_items.items():
    value.print_self()