from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hashPassword(password:str):
    return password_hash.hash(password)

def verifyHashPassword(plainPassword:str,hashedPassword):
    return password_hash.verify(plainPassword,hashedPassword)