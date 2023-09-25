import requests
import json
from enum import Enum
import re
from urllib.parse import unquote, quote

import pandas as pd



#use regex expressions to clean up the market_name for the MarketplaceItem: Gun: .... Skin .... Quality .... Stattrak T/F

# Goal for this project
# - fill out an excel sheet or google sheet with gun names and the price I paid for each item
# - use this code to find the current prices for all those items
# - count how much I'm profiting assuming a 20% market cut when sold
# - draw a graph of my asset value
#

#
# - Fix Excel formatting issues maybe use something else instead of pandas
#

marketplace_items = {}

class AppID(Enum):
    csgo = "730"
    tf2 = "440"
    
class MarketName(Enum):
    FT_AK_REDLINE = "AK-47%20%7C%20Redline%20%28Field-Tested%29"
    ST_FT_AK_REDLINE = "StatTrak™%20AK-47%20%7C%20Redline%20%28Field-Tested%29"
    AK_HEADSHOT = "AK-47%20%7C%20Head%20Shot%20%28Field-Tested%29"
    AK_LEETMUSEO = "AK-47%20%7C%20Leet%20Museo%20%28Factory%20New%29"
    
    
    
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

class MyItem:
    def __init__(self, paid_price: float, market_name: str, quanitity: int = 1):
        self.paid_price = paid_price
        self.current_market_value = 0
        self.market_name = market_name
        self.quantity = quanitity #how many of this item do you have
        
        self.marketplaceitem = None
    
    def update_price(self):
        temp = get_item_info("730",self.market_name,"20")
        self.current_market_value = temp["lowest_price"]
        self.marketplaceitem = MarketPlaceItem(temp["name"],temp["lowest_price"],temp["volume"],temp["median_price"],temp["wear"],temp["stattrak"])
    
    def print(self):
        print(f"I paid: CDN$ {self.paid_price} || item costs: {self.current_market_value}")


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
            
            return{
                "name" : gun_name,
                "lowest_price" : data["lowest_price"],
                "median_price": data["median_price"],
                "volume": data["volume"],
                "wear": wear,
                "gun_name": gun_name,
                "stattrak": statTrak
                
            }
            
        else:
            print ("Failed to fetch data")
    
    else:
        print(f"HTTP Error {response.status_code}")
        



def write_to_excel():
    # Create a sample DataFrame
    data = [
    ]
    for key, value in marketplace_items.items():
        data.append([f"{key}",f"{value.lowest_price}",f"{value.wear}"])
    df = pd.DataFrame(data)

    # Write the DataFrame to Excel
    df.to_excel('output.xlsx', index=False, engine='openpyxl')




my_items = {
    "ak_blue_laminate" : MyItem(31.20,"StatTrak™%20AK-47%20%7C%20Blue%20Laminate%20(Minimal%20Wear)"),
    "m4a4_living_color" : MyItem(24.96,"StatTrak™%20M4A4%20%7C%20In%20Living%20Color%20(Field-Tested)"),
    "ak_elite_build" : MyItem(6.58,"StatTrak™%20AK-47%20%7C%20Elite%20Build%20(Well-Worn)"),
    "ak_leet_museo" : MyItem(0,"StatTrak™%20AK-47%20%7C%20Leet%20Museo%20(Field-Tested)"),
}


if __name__ == '__main__':
    for key, value in my_items.items():
        value.update_price()
        value.print()
    # get_item_info(AppID.csgo.value, MarketName.ST_FT_AK_REDLINE.value, Currency.CAD.value)
    # get_item_info(AppID.csgo.value, MarketName.FT_AK_REDLINE.value, Currency.CAD.value)
    # get_item_info(AppID.csgo.value, MarketName.AK_HEADSHOT.value, Currency.CAD.value)
    # get_item_info(AppID.csgo.value, MarketName.AK_LEETMUSEO.value, Currency.CAD.value)
    
    # write_to_excel()
    
    