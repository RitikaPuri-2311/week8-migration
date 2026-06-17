from app.jwt_handler import (
    create_access_token,
    verify_token
)

import time

token = create_access_token(
    {
        "sub": "ritika@gmail.com"
    }
)

print("Generated Token:\n")
print(token)


payload = verify_token(token)

print("\nDecoded Payload:\n")
print(payload)

'''
print("\nVerifying immediately:")
print(verify_token(token))

print("\nWaiting 15 seconds...")
time.sleep(15)

print("\nVerifying again:")
print(verify_token(token))
'''