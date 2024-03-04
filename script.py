import urllib.request
import json
import pandas as pd
import sys

def fetch_menu_data(restaurant_id):
    url = f"https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=18.56&lng=73.95&restaurantId={restaurant_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            menu_data = json.loads(data)
            return menu_data
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        sys.exit(1)

def extract_menu_details(menu_data):
    menu_details = []
    for item in menu_data['menu_items']:
        name = item['name']
        price = item['price']
        description = item['description']
        category = item['category']
        menu_details.append({'Name': name, 'Price': price, 'Description': description, 'Category': category})
    return menu_details

def save_to_csv(menu_details, restaurant_id):
    df = pd.DataFrame(menu_details)
    df.to_csv(f"{restaurant_id}_menu.csv", index=False)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py restaurant_id")
        sys.exit(1)

    restaurant_id = sys.argv[1]
    
    menu_data = fetch_menu_data(restaurant_id)
    menu_details = extract_menu_details(menu_data)
    
    if not menu_details:
        print("No menu details found.")
        sys.exit(1)
    
    save_to_csv(menu_details, restaurant_id)
    print(f"Menu data saved to {restaurant_id}_menu.csv")

if __name__ == "__main__":
    main()

