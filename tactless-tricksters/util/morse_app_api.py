import requests


class MorseAppApi(object):
    def __init__(self, util, auth_token=None):
        self.util = util
        self.auth_token = auth_token
        self.logged_in = True if auth_token else False
        self.header = {'Authorization': 'Token %s'} % self.auth_token
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
        self.query_user = 'api/user/%s'

        # Send message
        # POST request only
        # data format dict {'sender': <user name>,'receiver': <user name>, 'message': <text>}
        # header required {'Authorization: 'access_token #########'}
        # return value {'sender':<>,'receiver':<>, 'message':<> 'time_stamp':<>}
        self.send_message = 'api/message'

        # Receive message
        # GET request only
        # must add user to api url like api/message/Blue42/Red87 to receive conversations
        # header required {'Authorization: 'access_token #########'}
        # return value {'sender':<>,'receiver':<>, 'message':<> 'time_stamp':<>}
        self.get_message = 'api/message/%s/%s' # sender/receiver

    def update_header(self, token):
        self.auth_token = token
        self.logged_in = True if token else False
        self.header = {'Authorization': 'Token %s'} % self.auth_token

    def create_user_req(self, username, password):
        data = {'username': username, 'password': password}
        url = self.base_url + self.create_user
        return self._handle_post_req(url=url, data=data)

    def retrieve_token_req(self, username, password):
        data = {'username': username, 'password': password}
        url = self.base_url + self.retrieve_token
        outs = self._handle_post_req(url=url, data=data)
        if str(outs.status_code) == '200':
            token = outs.content['token']
            self.update_header(token)
            return True
        else:
            return False

    def query_user_req(self, username):
        header = self.header
        url = self.query_user % username
        outs = self._handle_get_req(url=url, header=header)
        if str(outs.status_code) == '200':
            return True
        else:
            return False

    def send_message_req(self, sender, receiver, message):
        header = self.header
        data = {'sender': sender, 'receiver': receiver, 'message': message}
        url = self.send_message
        outs = self._handle_get_req(url=url, header=header, data=data)
        if str(outs.status_code) == '200':
            return True
        else:
            return False

    def get_message_req(self, sender, receiver):
        header = self.header
        url = self.get_message % (sender, receiver)
        outs = self._handle_get_req(url=url, header=header, data=data)
        if str(outs.status_code) == '200':
            return outs.content
        else:
            return False

    def _handle_get_req(self, url, header=None, data=None):
        try:
            print('Send GET Request %s' % url)
            outs = requests.get(url=url, header=header, data=data)
            print('GET Response: %s' % outs.content)
            if str(outs.status_code) in ['200', '201']:  # TODO Fix all the 201s to 200
                return outs.content
            else:
                return None
        except requests.exceptions.HTTPError as errh:
            print("An Http Error occurred:" + repr(errh))
        except requests.exceptions.ConnectionError as errc:
            print("An Error Connecting to the API occurred:" + repr(errc))
        except requests.exceptions.Timeout as errt:
            print("A Timeout Error occurred:" + repr(errt))
        except requests.exceptions.RequestException as err:
            print("An Unknown Error occurred" + repr(err))
        return None

    def _handle_post_request(self, url, header=None, data=None):
        try:
            print('Send POST Request %s with Data %s' % (url, data))
            outs = requests.post(url=url, header=header, data=data)
            print('POST Response: %s' % outs.content)
            if str(outs.status_code) in ['200', '201']:  # TODO Fix all the 201s to 200
                return outs.content
            else:
                return None
        except requests.exceptions.HTTPError as errh:
            print("An Http Error occurred:" + repr(errh))
        except requests.exceptions.ConnectionError as errc:
            print("An Error Connecting to the API occurred:" + repr(errc))
        except requests.exceptions.Timeout as errt:
            print("A Timeout Error occurred:" + repr(errt))
        except requests.exceptions.RequestException as err:
            print("An Unknown Error occurred" + repr(err))
        return None
