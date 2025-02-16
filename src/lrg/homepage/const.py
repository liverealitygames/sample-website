from geosky import geo_plug

ACCOUNT_STATUSES = [
    "Active",
    "Banned",
    "Suspended",
    "Muted",
]

AUTH_SOURCES = [
    "Internal",  # Made an account owned by LRG with email/password
]

VALID_COUNTRIES = geo_plug.all_CountryNames() + ["Online"]