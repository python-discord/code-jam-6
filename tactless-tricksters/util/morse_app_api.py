import json

from kivy.network.urlrequest import UrlRequest


class MorseAppApi(object):
    def __init__(self, util, auth_token=None):
        self.util = util
        self.auth_token = auth_token
        self.logged_in = True if auth_token else False
        self.header = {'Authorization': 'Token %s' % self.auth_token,
                       'Content-type': 'application/json'}
        self.base_url = 'https://yangpinkhats2020.com/'

        # Create User
        # POST request only
        # data format dict {'username': <user name>,'password': <password>}
        # Returns {'error':'User Already exists'} if user exists
        self.create_user = 'api/create_user'

        # Retrieve Token
        # POST request only
        # data format dict {'username': <user name>,'password': <password>}
        # returns {'token': <token>}
        self.retrieve_token = 'api/token-auth'

        # Query User
        # GET Request only
        # must add user to api url like api/user/Blue42 to send user info
        # header required {'Authorization: 'access_token #########'}
        # returns error's 'Must Supply User Name' (no user name given)
        # and 'User not found'
        self.query_user = 'api/user/'

        # Send message
        # POST request only
        # data format dict {'sender': <user name>,'receiver': <user name>, 'message': <text>}
        # header required {'Authorization: 'access_token #########'}
        # return value {'sender':<>,'receiver':<>, 'message':<> 'time_stamp':<>}
        self.send_message = 'api/messages'

        # Receive message
        # GET request only
        # must add user to api url like api/message/Blue42/Red87 to receive conversations
        # header required {'Authorization: 'access_token #########'}
        # return value {'sender':<>,'receiver':<>, 'message':<> 'time_stamp':<>}
        self.get_message = 'api/messages/'  # /sender/receiver

    def update_header(self, token):
        self.auth_token = token
        self.logged_in = True if token else False
        self.header = {'Authorization': 'Token %s' % self.auth_token,
                       'Content-type': 'application/json'}
        print('Token %s' % token)

    def create_user_req(self, callback, username, password):
        data = json.dumps({'username': username, 'password': password})
        url = self.base_url + self.create_user
        header = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        self._handle_post_req(callback, url=url, header=header, data=data)

    def retrieve_token_req(self, callback, username, password):
        data = json.dumps({'username': username, 'password': password})
        url = self.base_url + self.retrieve_token
        header = {'Content-type': 'application/json'}
        self._handle_post_req(callback, url=url, header=header, data=data)

    def query_user_req(self, callback, username):
        header = self.header
        url = self.base_url + self.query_user + username
        self._handle_get_req(callback, url=url, header=header)

    def send_message_req(self, callback, sender, receiver, message):
        header = self.header
        data = json.dumps({'sender': sender, 'receiver': receiver, 'message': message})
        url = self.base_url + self.send_message
        self._handle_post_req(callback, url=url, header=header, data=data)

    def get_message_req(self, callback, sender, receiver):
        header = self.header
        url = self.base_url + self.get_message + sender + '/' + receiver
        self._handle_get_req(callback, url=url, header=header)

    def _handle_get_req(self, callback, url, header=None, data=None):
        UrlRequest(url, method='GET', req_headers=header,
                   req_body=data, on_success=callback,
                   on_error=callback, on_failure=callback)

    def _handle_post_req(self, callback, url, header=None, data=None):
        UrlRequest(url, req_headers=header, req_body=data,
                   on_success=callback, on_error=callback,
                   on_failure=callback)
