import jwt
import datetime
import time
from datetime import timedelta

key = "django-insecure-co&qhn&q2*%rg3491&*5#l9ts=fj2$a^mcha)h1_76n8hfg%dc"

print('now=', datetime.datetime.now())

dt = datetime.datetime.now() + timedelta(seconds=10)

print('now with 5 minutes=',dt)



payload = {'video_id': "1", 'lesson_id': "1"}
expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=10)
payload['exp'] = int(expiration_time.timestamp())

encoded_token = jwt.encode(payload, key, algorithm='HS256')
print(encoded_token)
decoded_token = jwt.decode(encoded_token, key, algorithms=['HS256'])
print(decoded_token)

# Wait for 15 seconds to simulate the token expiring
time.sleep(10)
# print(decoded_token)
# Attempt to decode the token again
try:
    decoded_token = jwt.decode(encoded_token, key, algorithms=['HS256'])
    print(decoded_token)
except jwt.ExpiredSignatureError:
    print('Token has expired')
