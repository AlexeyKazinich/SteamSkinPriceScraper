import requests
import json
from enum import Enum

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
    ChromaCaseKey = "Chroma%202%20Case%20Key"
    AWP = "AWP%20%7C%20Elite%20Build%20%28Minimal%20Wear"
    case = "Revolution%20Case"
    ak = "AK-47%20%7C%20Redline%20%28Field-Tested%29"

class MarketPlaceItem:
    def __init__(self,name = str, lowest_price = str, volume = str, median_price = str):
        self.name = name
        self.volume = volume
        self.lowest_price = lowest_price
        self.median_price = median_price
    
    def print_self(self):
        print(f"name: {self.name} || price: {self.lowest_price}")

class Currency(Enum):
    USD = "1"
    CAD = "20"
    

def get_item_info(app_id: str,market_name: str, currency : str):
    url = f"https://steamcommunity.com/market/priceoverview/?appid={app_id}&market_hash_name={market_name}&currency={currency}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        marketplace_items[market_name] = MarketPlaceItem(market_name,data["lowest_price"],data["volume"],data["median_price"])
        
        if 'success' in data and data['success']:
            marketplace_items[market_name].print_self()
            
        else:
            print ("Failed to fetch data")
    
    else:
        print(f"HTTP Error {response.status_code}")

get_item_info(AppID.csgo.value,MarketName.ak.value,Currency.CAD.value)