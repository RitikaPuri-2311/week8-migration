from app.auth import (
    hash_password,
    verify_password
)

password = "admin123"

hashed = hash_password(password)

print("Original:", password)
print("Hash:", hashed)

is_valid = verify_password(
    password,
    hashed
)

print("Valid:", is_valid)