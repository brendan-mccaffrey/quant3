import os
import asyncio
import websockets
from dotenv import load_dotenv, find_dotenv

# load environment variables
load_dotenv(find_dotenv()) 


class WsClient:
    '''Superchain API WS Client'''

    base_url = "wss://partners.superchain.app/api/eth/ws"

    def __init__(self):
        '''Constructor'''
        self.auth_key = os.getenv("AUTH")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")