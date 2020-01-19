from kivy.uix.screenmanager import Screen
from requests import get


def get_wiki_summary() -> str:
    endpoint = "https://en.wikipedia.org/w/api.php?action=query&list=random&" \
               "format=json&rnnamespace=0&rnlimit=1&origin=*"
    response = get(endpoint)
    title = (response.json())["query"]["random"][0]["title"]
    endpoint = "https://en.wikipedia.org/api/rest_v1/page/summary/"
    response1 = get(endpoint + title.replace(" ", "%20"))
    return response1.json()["extract"]


class PaperScreen(Screen):
    pass
