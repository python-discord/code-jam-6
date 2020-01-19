from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore


class GameScreen(Screen):
    store = JsonStore("data/sample/hello.json")
    store.put("blah", name="Blah", org="kivy")
    store.put('tshirtman', name='Gabriel', age=27)
    store.put('tito', name='Mathieu', age=30)
    print('tito is', store.get('tito')['age'])

    # or guess the key/entry for a part of the key
    for item in store.find(name='Gabriel'):
        print('tshirtmans index key is', item[0])
        print('his key value pairs are', str(item[1]))
