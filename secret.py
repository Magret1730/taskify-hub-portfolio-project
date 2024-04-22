import os

# Generate a secret key
secret_key = os.urandom(24)

print(secret_key.hex())
