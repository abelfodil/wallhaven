BASE_URL = "https://wallhaven.cc"
API_URL = BASE_URL + "/api/v1"

ROUTES = {
    "wallpaper": API_URL + "/w/" + "{id}",
    "tag": API_URL + "/tag/" + "{id}",
    "settings": API_URL + "/settings",  # ?apikey=<api_key>
    "collections_username": API_URL + "/collections/" + "{username}",
    "collections_apikey": API_URL + "/collections",  # ?api_key=<api_key>
    "collection_wallpapers": API_URL + "/collections/" + "{username}/{id}",
}
