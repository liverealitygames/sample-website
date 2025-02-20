import geonamescache 

gc = geonamescache.GeonamesCache()
COUNTRIES: dict = { country_short:obj['name'] for country_short, obj in gc.get_countries().items() }
CITIES: dict = list(gc.get_cities().keys())
STATES: dict = { region_short:obj['name'] for region_short, obj in gc.get_us_states().items() }