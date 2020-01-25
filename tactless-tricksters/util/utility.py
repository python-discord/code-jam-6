from third_party.py_morse_code.morse import Morse, DotDash
from auto_morse_recognizer.auto_morse_recognizer import AutoMorseRecognizer
from threading import Thread

message_dict ={'Bob': {
                                'messages': [
                                            {
                                                'text':"The 2019–20 NBA season is the 74th season of the National Basketball Association (NBA). The regular season began on October 22, 2019 and will end on April 15, 2020. The playoffs will begin on April 18, 2020, and will end with the NBA Finals in June 2020. The 2020 NBA All-Star Game will be played on February 16, 2020, at the United Center in Chicago, Illinois.",
                                                'author':'user_name',
                                                'date':'111111'
                                            },
                                            {
                                                'text': "The National Football League (NFL) is a professional American football league consisting of 32 teams, divided equally between the National Football Conference (NFC) and the American Football Conference (AFC). The NFL is one of the four major professional sports leagues in North America and the highest professional level of American football in the world.[3] The NFL's 17-week regular season runs from early September to late December, with each team playing 16 games and having one bye week. Following the conclusion of the regular season, six teams from each conference (four division winners and two wild card teams) advance to the playoffs, a single-elimination tournament culminating in the Super Bowl, which is usually held on the first Sunday in February and is played between the champions of the NFC and AFC.,",
                                                'author': 'Bob',
                                                'date': '222222'
                                            },
                                            {
                                                'text': 'foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo',
                                                'author': 'Bob',
                                                'date': '333333'
                                            },
                                            ],
                                'img_source': 'ui/img/default_avatar.png',
                                }
                             ,
                             'Rob': {
                                'messages': [
                                             {
                                                 'text': 'hello1',
                                                 'author': 'user_name',
                                                 'date': '111111'
                                             },
                                             {
                                                 'text': 'world1',
                                                 'author': 'Rob',
                                                 'date': '222222'
                                             },
                                             {
                                                 'text': 'foo1',
                                                 'author': 'Rob',
                                                 'date': '333333'
                                             },
                                            ],
                             'img_source': 'ui/img/default_avatar.png',
                                },
                            'Rod': {
                                'messages': [
                                            {
                                                'text': 'hello2',
                                                'author': 'user_name',
                                                'date': '111111'
                                            },
                                            {
                                                'text': 'world2',
                                                'author': 'Rob',
                                                'date': '222222'
                                            },
                                            {
                                                'text': 'foo2',
                                                'author': 'Rob',
                                                'date': '333333'
                                            },
                                            ],
                             'img_source': 'ui/img/default_avatar.png',
                                }
                            }

contact_list = ['Bob', 'Rob', 'Rod']

class Utility(object):
    def __init__(self):
        self.user_name = 'user_name'
        self.morse = Morse()
        # Temp debug data
        self.message_dict = message_dict
        self.contact_list = contact_list
        self.morse = Morse()
        self.auto_morse_recognizer = AutoMorseRecognizer(active_threshold=9)


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
