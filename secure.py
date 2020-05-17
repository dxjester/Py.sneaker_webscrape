from cryptography.fernet import Fernet

key = Fernet.generate_key()
key

f = Fernet(key)
f

token = f.encrypt(b"A really secret message. Not for prying eyes.")
token

f.decrypt(token)
