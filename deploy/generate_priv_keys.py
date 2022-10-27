import secrets
for i in range(0, 10):
    priv_key = secrets.token_hex(32)
    print(i+1, ': ', priv_key)
