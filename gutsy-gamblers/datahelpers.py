import requests

LOCATION_FRIENDLY = 'location_friendly'
LOCATION_LATLON = 'location_latlon'
LOCATION_VALID = 'location_valid'


FAKE_DATA = False


def commaval_or_empty(src: dict, key: str) -> str:
    """
    Returns f", {value}" or '' if there's no value in the dict
    :param src: dict to fetch from
    :param key: key to get value from
    :return: str
    """
    if key in src:
        return f", {src[key]}"
    return ''


def guess_location_by_ip() -> dict:
    """
    Guess location by IP

    Needs more work in case of failure conditions
    :return:
    """
    if FAKE_DATA:
        return {
            'location_latlon': '40.730610,-73.935242',
            'location_friendly': 'New York City, NY, United States'}

    try:
        resp = requests.get('http://ip-api.com/json/').json()
    except ConnectionError:
        return None

    location = {}

    location[LOCATION_LATLON] = f"{resp['lat']},{resp['lon']}"

    friendly_name = resp.get('city')
    friendly_name += commaval_or_empty(resp, 'region')
    friendly_name += commaval_or_empty(resp, 'country')
    # including ZIP might be too long
    # friendly_name += commaval_or_empty(resp, 'zip')

    location[LOCATION_FRIENDLY] = friendly_name

    return location
