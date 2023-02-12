import re
import base64


text = "hello world"

def basic_auth(password):
    token = password = base64.b64encode(password.encode()).decode('ascii')
    return token

password = input()
hashed_password = basic_auth(password=password)
print(hashed_password)
