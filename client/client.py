import os
import requests
from dotenv import load_dotenv

load_dotenv() # take environment variables from .env.

class SuperchainClient:
    '''Superchain API HTTP Client'''

    base_url = "https://partners.superchain.app/v1/api/"

    def __init__(self):
        '''Constructor'''
        self.auth_key = os.getenv("AUTH")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")

    def make_header(self):
        '''Constructs authorization header.'''
        return { "Authorization" : "Basic " + self.auth_key }

    def handle_response(self, response):
        if response.status_code == 200:
            # Success!
            data = response.json()
            return data
        else:
            # There was an error
            print(f"Error: {response.status_code}")

    def get_height(self):
        '''Get the current block height.'''
        url = self.base_url + "eth/height"
        headers = self.make_header()
        response = requests.get(url, headers=headers)
        return self.handle_response(response)

    def get_trades(self, pair, start=None, stop=None):
        '''Get trades for a given pair, start & stop blocks are optional.'''
        # TODO: Add start & stop blocks
        url = self.base_url + "eth/trades/" + pair
        headers = self.make_header()
        response = requests.get(url, headers=headers)
        return self.handle_response(response)


