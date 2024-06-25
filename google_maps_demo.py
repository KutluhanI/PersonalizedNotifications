import requests

# Google Maps API Key
API_KEY = 'AIzaSyAxY_KanX1B79-48-m6XVBV6Bjr5lN4254'

def get_nearby_shops(location, radius=3):
    lat, lng = location
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=store&key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Unable to fetch data from Google Maps API, status code: {response.status_code}")
        return []

    data = response.json()
    if 'error_message' in data:
        print(f"Error from API: {data['error_message']}")
        return []

    results = data.get('results', [])
    print(f"API Response: {results}") 
    shops = []
    for result in results:
        shop_name = result.get('name', 'Unknown')
        geometry = result.get('geometry', {})
        location = geometry.get('location', {})
        shop_lat = location.get('lat', lat) 
        shop_lng = location.get('lng', lng) 
        shops.append((shop_name, (shop_lat, shop_lng)))
    
    if not shops:
        print("No shops found.")
    
    return shops

def demo_google_maps(location):
    nearby_shops = get_nearby_shops(location)
    print(f"Nearby shops for location {location}:")
    for shop_name, shop_location in nearby_shops:
        print(f"{shop_name}")

location = (37.7749, -122.4194) 
demo_google_maps(location)
