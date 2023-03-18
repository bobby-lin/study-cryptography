"""
Exercise: https://aes.cryptohack.org/ecb_oracle/
"""
import requests
from binascii import hexlify as hexa
import string

BLOCK_SIZE = 32


def split_blocks(hex_data):
    split_arr = [hex_data[i:i + BLOCK_SIZE] for i in range(0, len(hex_data), BLOCK_SIZE)]
    return split_arr


def encrypt(plaintext, iv):
    url = f'https://aes.cryptohack.org/symmetry/encrypt/{plaintext}/{iv}/'
    response = requests.get(url)
    return response.json()['ciphertext']


def encrypt_flag():
    url = f'https://aes.cryptohack.org/symmetry/encrypt_flag/'
    response = requests.get(url)
    return response.json()['ciphertext']


encrypted_flag = encrypt_flag()
block_arr = split_blocks(encrypted_flag)
iv = block_arr[0]
ciphertext = encrypted_flag.replace(iv, '')
print(block_arr)
print(iv, ciphertext)


GUESS_FLAG = 'crypto{'
print(encrypt(GUESS_FLAG.encode().hex(), iv))

while True:
    if b'}' in GUESS_FLAG.encode():
        break

    guess_encrypted_flag = encrypt(GUESS_FLAG.encode().hex(), iv)

    for ch in string.printable:
        current_flag_guess = GUESS_FLAG.encode() + ch.encode()

        guess_encrypted_flag = encrypt(current_flag_guess.hex(), iv)

        if guess_encrypted_flag in encrypted_flag:
            print(guess_encrypted_flag, encrypted_flag)
            GUESS_FLAG += ch
            print(GUESS_FLAG)