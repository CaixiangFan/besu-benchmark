import secrets
import json

# priv_keys = []
# with open('ibftConfigFile-template.json') as file_read:
#     data = json.load(file_read)
#     print(data['genesis']['alloc'])

for i in range(0, 10):
    priv_key = secrets.token_hex(32)
    print(i+1, ': ', priv_key)
