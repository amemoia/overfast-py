import requests

def get(type: str, locale: str = "en-us", key: str = None):
    """Get any OverFast data except players.
    Cache TTL may vary, see https://overfast-api.tekrop.fr/"""
    url = "https://overfast-api.tekrop.fr/"
    params = {}
    types = ["hero", "heroes", "gamemodes", "maps"]
    if type not in types:
        return "Invalid type argument. Available types: " + ", ".join(types)
    
    if type == "hero":
        if not key:
            type = "heroes"
        else:
            type = "heroes/" + key
    if type in ['hero', 'heroes', 'gamemodes']:
        params["locale"] : locale
    if type == "maps":
        if key:
            params["gamemode"] = key
    
    data = requests.get(url + type, params)
    response = data.json()

    if data.status_code != 200:
        if data.status_code == 422:
            return "Validation error"
        else:
            
            return response["error"]
    else:
        return response
    
def player(type: str = None, name: str = None, id: str = None,
            privacy: str = None, order_by: str = None, offset: str=None,
            limit: str=None, gamemode: str = None, platform: str = None, hero: str = None):
    """Get player data from the OverFast API.
        Cache TTL may vary. Requests accept different arguments:
            No type (search by name): name (required)
            summary: player id (required)
            stats_summary: player id (required), gamemode, platform
            stats_career: player id (required), gamemode, platform, hero
            stats: player id (required), gamemode, platform, hero
            all: player_id (required)"""
    types = ["summary", "stats_summary", "stats_career", "stats", "all"]
    url = "https://overfast-api.tekrop.fr/" + "players"
    params = {} # The dict we send as our parameters
    args = [] # The key names of the values we'll send over

    if id != None and type == None:
        type = "summary"
    if type and type not in types:
        return "Invalid type argument. Available types: " + ", ".join(types)
    if type == "all":
        # Evil hack to fix the URL
        type = ""

    if type != None:
        if not id:
            return "A player id is required."
        if type == "stats_summary":
            args.extend(["gamemode", "platform"])
        elif type in ["stats_career", "stats"]:
            args.extend(["gamemode", "platform", "hero"])
        id = id.replace("#", "-")
        type = type.replace("_", "/")
        url = url + "/" + id + "/" + type
    else:
        args.extend(["name", "privacy", "order_by", "offset", "limit"])
        if not name:
            return "A player name is required."
    keys = {}
    for key, val in list(locals().items()):
        if locals()['key'] != None:
            keys[key] = val
    for x in keys:
        if locals().get(x) != None:
            if x in args:
                params[x] = locals().get(x)

    data = requests.get(url, params)
    response = data.json()
    if data.status_code != 200:
        if data.status_code == 422:
            return "Validation error: " + str(response)
        else:
            return response["error"]
    else:
        return response
        