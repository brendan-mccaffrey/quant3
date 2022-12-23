import requests
import asyncio
import websockets


def http_make_header():
    endpoint = "wss://partners.superchain.app/api/eth/ws"
    auth_type = "Basic"
    auth_key = "dW5kZWZpbmVkOjM5YmU2MmExNmEwOTI4NjdjMzczYTAzNDNmNDJjNTRh"
    pragma = "no-cache"


def http_example_request():
    message = {
        "subscription": {
            address: "0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc",
            command: "subscribe",
            dataType: "full",
        }
    }


def http_send_request():
    endpoint = "wss://partners.superchain.app/api/eth/ws"


async def ws_request():
    headers = {
        "Authorization": "Basic dW5kZWZpbmVkOjM5YmU2MmExNmEwOTI4NjdjMzczYTAzNDNmNDJjNTRh",
    }

    async with websockets.connect(
        "wss://partners.superchain.app/api/eth/ws", headers=headers
    ) as ws:
        send_msg(ws)


async def send_msg(ws):
    payload = {
        address: "0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852",
        command: "subscribe",
        dataType: "full",
    }
    await ws.send(payload)
    response = await ws.recv()
    print("Got Response!")
    print(response)


loop = asyncio.get_event_loop()
loop.run_until_complete(ws_request)
