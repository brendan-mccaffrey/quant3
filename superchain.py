from superchain import client

cl = client.HTTPClient()

print(cl.get_height())