from cryptography.fernet import Fernet
# Put this somewhere safe!
print("Test")
key = Fernet.generate_key()
key
f = Fernet(key)
f

token = f.encrypt(b"A really secret message. Not for prying eyes.")
token

f.decrypt(token)
