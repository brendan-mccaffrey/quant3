import requests
import base64

BASE_URL = "https://partners.superchain.app/v1"
USERPASS = "undefined:39be62a16a092867c373a0343f42c54a"
AUTH = "dW5kZWZpbmVkOjM5YmU2MmExNmEwOTI4NjdjMzczYTAzNDNmNDJjNTRh"


def trades_endpoint(pair):
    return BASE_URL + "/api/eth/trades/" + pair


def encoded_header():
    header = {"Authorization": "Basic " + AUTH}
    return header


def header():
    return {"Authorization": "Basic " + USERPASS}


def make_request():
    url = trades_endpoint("0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852")
    headers = header()
    response = requests.get(url, headers=headers)

    print(url)
    print(headers)

    if response.status_code == 200:
        # Success!
        data = response.json()
    else:
        # There was an error
        print(f"Error: {response.status_code}")
        if response.status_code == 401:
            print(" > Unauthorized")


print(encoded_header())
# make_request()
