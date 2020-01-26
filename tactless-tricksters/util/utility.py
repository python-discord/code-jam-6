from kivy.utils import platform
from kivy.clock import Clock
from kivy.app import App
if platform not in ['ios', 'android']:
    from third_party.py_morse_code.morse import Morse, DotDash
    from auto_morse_recognizer.auto_morse_recognizer import AutoMorseRecognizer
else:
    # Add mobile support later
    pass
from util.morse_app_api import MorseAppApi
from threading import Thread
import os
import json
from functools import partial
# message_dict ={'Bob': {
#                                 'messages': [
#                                             {
#                                                 'text':"The 2019–20 NBA season is the 74th season of the National Basketball Association (NBA). The regular season began on October 22, 2019 and will end on April 15, 2020. The playoffs will begin on April 18, 2020, and will end with the NBA Finals in June 2020. The 2020 NBA All-Star Game will be played on February 16, 2020, at the United Center in Chicago, Illinois.",
#                                                 'author':'user_name',
#                                                 'date':'111111'
#                                             },
#                                             {
#                                                 'text': "The National Football League (NFL) is a professional American football league consisting of 32 teams, divided equally between the National Football Conference (NFC) and the American Football Conference (AFC). The NFL is one of the four major professional sports leagues in North America and the highest professional level of American football in the world.[3] The NFL's 17-week regular season runs from early September to late December, with each team playing 16 games and having one bye week. Following the conclusion of the regular season, six teams from each conference (four division winners and two wild card teams) advance to the playoffs, a single-elimination tournament culminating in the Super Bowl, which is usually held on the first Sunday in February and is played between the champions of the NFC and AFC.,",
#                                                 'author': 'Bob',
#                                                 'date': '222222'
#                                             },
#                                             {
#                                                 'text': 'foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo',
#                                                 'author': 'Bob',
#                                                 'date': '333333'
#                                             },
#                                             ],
#                                 'img_source': 'ui/img/default_avatar.png',
#                                 }
#                              ,
#                              'Rob': {
#                                 'messages': [
#                                              {
#                                                  'text': 'hello1',
#                                                  'author': 'user_name',
#                                                  'date': '111111'
#                                              },
#                                              {
#                                                  'text': 'world1',
#                                                  'author': 'Rob',
#                                                  'date': '222222'
#                                              },
#                                              {
#                                                  'text': 'foo1',
#                                                  'author': 'Rob',
#                                                  'date': '333333'
#                                              },
#                                             ],
#                              'img_source': 'ui/img/default_avatar.png',
#                                 },
#                             'Rod': {
#                                 'messages': [
#                                             {
#                                                 'text': 'hello2',
#                                                 'author': 'user_name',
#                                                 'date': '111111'
#                                             },
#                                             {
#                                                 'text': 'world2',
#                                                 'author': 'Rob',
#                                                 'date': '222222'
#                                             },
#                                             {
#                                                 'text': 'foo2',
#                                                 'author': 'Rob',
#                                                 'date': '333333'
#                                             },
#                                             ],
#                              'img_source': 'ui/img/default_avatar.png',
#                                 }
#                             }
#
# contact_list = ['Bob', 'Rob', 'Rod']

base_file_json = {
    'username': '',
    'token': '',
    'contacts': [],
    'message_dict': {}
}

class Utility(object):
    def __init__(self):
        self.user_data_json = 'data/user_data.json'
        if not os.path.exists(self.user_data_json):
            # Not really removing, just making a blank template
            self.remove_user_data()
        with open(self.user_data_json, 'r') as fp:
            self.user_data = json.load(fp)
        self.username = self.user_data['username']
        self.auth_token = self.user_data['token']
        self.contact_list = self.user_data['contacts']
        self.message_dict = self.user_data['message_dict']
        self.calibration = 0.5
        self.morse_app_api = MorseAppApi(self, self.auth_token)
        self.morse = Morse()
        # Temp debug data
        self.message_dict = {}
        Clock.schedule_interval(self.update_messages, 10)

        if platform not in ['ios', 'android']:
            self.morse = Morse()
            self.auto_morse_recognizer = AutoMorseRecognizer(active_threshold=self.calibration)

    def save_contact(self, contact):
        self.user_data['contacts'].append(contact)
        with open(self.user_data_json, 'w') as fp:
            json.dump(self.user_data, fp)

    def save_token(self, token):
        self.user_data['token'] = token
        self.auth_token = token
        with open(self.user_data_json, 'w') as fp:
            json.dump(self.user_data, fp)

    def save_username(self, username):
        self.user_data['username'] = username
        self.username = username
        with open(self.user_data_json, 'w') as fp:
            json.dump(self.user_data, fp)

    def save_message_dict(self, msg_dict):
        self.user_data['message_dict'] = msg_dict
        with open(self.user_data_json, 'w') as fp:
            json.dump(self.user_data, fp)

    def remove_user_data(self):
        with open(self.user_data_json, 'w') as fp:
            json.dump(base_file_json, fp)

    def reload_screen_layout(self, screen_name):
        for screen in App.get_running_app().root.content.screens:
            if screen.name == screen_name:
                screen.ui_layout()

    # This runs through out the entire app waiting to add more messages
    def update_messages(self, dt):
        if self.contact_list and self.username and self.auth_token:
            for contact in self.contact_list:
                self.morse_app_api.get_message_req(self.update_message_cb, self.username, contact)
                self.morse_app_api.get_message_req(self.update_message_cb, contact, self.username)

    def update_message_cb(self, request, result):
        if request.resp_status != 200:
            print('No data')
            return
        if result:
            for res in result:
                if res['sender'] == self.username:
                    if res['receiver'] in self.message_dict.keys():
                        if res not in self.message_dict[res['receiver']]:
                            self.message_dict[res['receiver']].append(res)
                    else:
                        self.message_dict[res['receiver']] = [res]
                else:
                    if res['receiver'] in self.message_dict.keys():
                        if res not in self.message_dict[res['sender']]:
                            self.message_dict[res['sender']].append(res)
                    else:
                        self.message_dict[res['sender']] = [res]
            self.save_message_dict(self.message_dict)


    def morse_transmit_thread(self):
        morse_thread = Thread(target=self.morse.transmit)
        morse_thread.daemon = True
        morse_thread.start()

    def morse_transmit_speak(self):
        morse_thread = Thread(target=self.morse.speak)
        morse_thread.daemon = True
        morse_thread.start()

    def load_messages(self):
        # TODO
        pass
