import os
import json
import requests
from utils.config import MENU_API_URL

def fetch_menu_data():
    response = requests.get(MENU_API_URL)
    response.raise_for_status()
    raw_json = response.json()

    # Check if 'data' exists and is a JSON string
    if "data" in raw_json:
        try:
            menu_json = json.loads(raw_json["data"])  # Parse the inner JSON string
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format inside 'data' field")
    else:
        raise ValueError("No 'data' field found in the API response")

    return menu_json

def extract_required_items(menu_json):
    extracted_items = []
    for category in menu_json.get("CategoryList", []):
        category_id = category.get("CategryId")
        category_name = category.get("CategryName")

        for item in category.get("ItemListWidget", []):
            item_obj = {
                "ItemId": item.get("ItemId"),
                "ItemName": item.get("ItemName"),
                "Description": item.get("Description", ""),
                "Price": item.get("Price"),
                "SizeId": item.get("SizeId"),
                "SizeListWidget": [],
                "CategoryId": category_id,
                "CategoryName": category_name
            }

            for size in item.get("SizeListWidget", []):
                size_obj = {
                    "SizeId": size.get("SizeId"),
                    "SizeName": size.get("SizeName"),
                    "Price": size.get("Price")
                }
                item_obj["SizeListWidget"].append(size_obj)

            extracted_items.append(item_obj)
    return extracted_items

def refresh_and_store_menu(file_path="data/parsed_menu.json"):
    menu = fetch_menu_data()
    cleaned = extract_required_items(menu)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(cleaned, f, indent=2)
    return cleaned

# Optional test
if __name__ == "__main__":
    menu_json = fetch_menu_data()
    cleaned_items = extract_required_items(menu_json)
    refresh_and_store_menu()
    print(json.dumps(cleaned_items, indent=2))