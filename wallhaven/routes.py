BASE_URL = "https://wallhaven.cc"
API_URL = BASE_URL + "/api/v1"

ROUTES = {
    "wallpaper": API_URL + "/w/" + "{id}",
    "tag": API_URL + "/tag/" + "{id}",
}
