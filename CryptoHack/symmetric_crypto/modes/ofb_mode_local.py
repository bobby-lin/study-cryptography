"""
Exercise: https://aes.cryptohack.org/symmetry/
"""
from Crypto.Cipher import AES
import os
import string

KEY = b'\xd1\x891\xb7\x1b\x0bM\xed\xc24\x1df\xed\x9a\xf9\x9d'
FLAG = 'crypto{xabcd123123132}'
iv = bytes.fromhex('c2c4c10ca295797fa15296fcfe616ed1')


def encrypt(plaintext, iv):
    plaintext = bytes.fromhex(plaintext)
    iv = bytes.fromhex(iv)
    if len(iv) != 16:
        return {"error": "IV length must be 16"}

    cipher = AES.new(KEY, AES.MODE_OFB, iv)
    encrypted = cipher.encrypt(plaintext)
    ciphertext = encrypted.hex()

    return {"ciphertext": ciphertext}


def encrypt_flag():
    cipher = AES.new(KEY, AES.MODE_OFB, iv)
    encrypted = cipher.encrypt(FLAG.encode())
    ciphertext = iv.hex() + encrypted.hex()

    return {"ciphertext": ciphertext}


GUESS_FLAG = 'crypto{'

print(encrypt(GUESS_FLAG.encode().hex(), iv.hex()))
encrypted_flag = encrypt_flag()['ciphertext']

"""
Bruteforce the choosen plaintext to check if the guess's ciphertext matches with the flag's ciphertext
"""
while True:
    if b'}' in GUESS_FLAG.encode():
        break

    guess_encrypted_flag = encrypt(GUESS_FLAG.encode().hex(), iv.hex())['ciphertext']

    for ch in string.printable:
        current_flag_guess = GUESS_FLAG.encode() + ch.encode()

        guess_encrypted_flag = encrypt(current_flag_guess.hex(), iv.hex())['ciphertext']

        if guess_encrypted_flag in encrypted_flag:
            print(guess_encrypted_flag, encrypted_flag)
            GUESS_FLAG += ch
            print(GUESS_FLAG)
