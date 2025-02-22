from cryptography.fernet import Fernet

key = Fernet.generate_key()
file = open("encryption key.text", "wb")
file.write(key)
file.close()