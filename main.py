import requests
import json

def fetch_steam_market_price(app_id, market_hash_name):
    url = f"https://steamcommunity.com/market/priceoverview/?appid={app_id}&market_hash_name={market_hash_name}&currency=1"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        
        if 'success' in data and data['success']:
            print(data)
            return data['lowest_price'], data['median_price']
        else:
            return "Failed to fetch data", "Failed to fetch data"
    else:
        return f"HTTP Error {response.status_code}", f"HTTP Error {response.status_code}"

# Example for CSGO item (Chroma 2 Case Key)
app_id = 730
market_hash_name = "Chroma%202%20Case%20Key"

lowest_price, median_price = fetch_steam_market_price(app_id, market_hash_name)

print(f"Lowest price: {lowest_price}")
print(f"Median price: {median_price}")