import argparse
import json
import os
import urllib.request
import urllib.parse

API_KEY = "563085f41fa4e69fc37940373402a4b0"
API_URL = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=imperial"
FAV_FILE = 'favorites.json'

favorites = []
if os.path.exists(FAV_FILE):
    with open(FAV_FILE, 'r') as file:
        favorites = json.load(file)

def save_favorites():
    with open(FAV_FILE, 'w') as file:
        json.dump(favorites, file)

def fetch_weather(city):
    try:
        url = API_URL.format(urllib.parse.quote(city), API_KEY)
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"Error fetching weather data for {city}: {e}")
        return None

def display_weather(data):
    return (
        f"Weather for {data['name']}:\n"
        f"Temperature: {data['main']['temp']}°F\n"
        f"Humidity: {data['main']['humidity']}%\n"
        f"Wind Speed: {data['wind']['speed']} mph\n"
    )

def add_to_favorites(city):
    if len(favorites) >= 3:
        print("Max cities limit reached!")
    elif city in favorites:
        print(f"{city} is already in favorites.")
    else:
        weather = fetch_weather(city)
        if weather:
            favorites.append(city)
            save_favorites()
            print(f"Added {city} to favorites.")
        else:
            print("Failed to fetch weather data.")

def update_favorite(old_city, new_city):
    if old_city in favorites:
        if new_city in favorites:
            print(f"{new_city} is already in favorites.")
        else:
            favorites[favorites.index(old_city)] = new_city
            save_favorites()
            print(f"Replaced {old_city} with {new_city}.")
    else:
        print(f"{old_city} not found in favorites.")

def main():
    parser = argparse.ArgumentParser(description="Weather and favorites management.")
    subparsers = parser.add_subparsers(dest='command')

    # Command: search
    parser_search = subparsers.add_parser('search', help="Search weather details")
    parser_search.add_argument('city_name', help="City name")

    # Command: add
    parser_add = subparsers.add_parser('add', help="Add city to favorites")
    parser_add.add_argument('city_name', help="City name")

    # Command: get
    parser_get = subparsers.add_parser('get', help="List favorite cities and their current weather")

    # Command: update
    parser_update = subparsers.add_parser('update', help="Update city in favorites")
    parser_update.add_argument('old_city', help="City to replace")
    parser_update.add_argument('new_city', help="New city")

    args = parser.parse_args()

    if args.command == 'search':
        weather = fetch_weather(args.city_name)
        if weather:
            print(display_weather(weather))
        else:
            print("Failed to fetch weather data.")

    elif args.command == 'add':
        add_to_favorites(args.city_name)

    elif args.command == 'get':
        if favorites:
            for city in favorites:
                weather = fetch_weather(city)
                if weather:
                    print(display_weather(weather))
                else:
                    print(f"Failed to fetch weather data for {city}.")
        else:
            print("No favorite cities.")

    elif args.command == 'update':
        update_favorite(args.old_city, args.new_city)

if __name__ == "__main__":
    main()