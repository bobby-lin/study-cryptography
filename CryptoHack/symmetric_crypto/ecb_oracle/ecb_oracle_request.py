"""
Exercise: https://aes.cryptohack.org/ecb_oracle/
"""
import requests
from binascii import hexlify as hexa
import string

BLOCK_SIZE = 16


def split_msg_to_blocks(data):
    split = [hexa(data[i:i+BLOCK_SIZE]) for i in range(0, len(data), BLOCK_SIZE)]
    return b' '.join(split)


def send_enc_req(plaintext):
    url = f'https://aes.cryptohack.org/ecb_oracle/encrypt/{plaintext}/'
    response = requests.get(url)
    return response.json()['ciphertext']


def guess(i, flag):
    plaintext = b'\x01' * i + flag
    c = send_enc_req(plaintext.hex())
    return split_msg_to_blocks(bytes.fromhex(c))


cipher_list = []


for i in range(1, 33):
    plaintext = b'\x01' * i
    c = send_enc_req(plaintext.hex())
    cipher_list.append(split_msg_to_blocks(bytes.fromhex(c)))
    print(f"Length of PT = {len(plaintext)} || C = {split_msg_to_blocks(bytes.fromhex(c))}")


# Quick check
# print(guess(1, current_flag_guess))

current_flag_guess = b''
i = 31  # Assuming 2 blocks (32 bytes) and flag is less than 32 bytes

while True:
    if i == 0 or b"}" in current_flag_guess:
        break
    for ch in string.printable:
        flag_guess = current_flag_guess + ch.encode()
        c = guess(i, flag_guess)
        for ct in cipher_list:
            # Increase number of concatenated blocks if the flag is > 32 bytes
            if ct.startswith(c.split(b" ")[0] + b" " + c.split(b" ")[1]):
                current_flag_guess = current_flag_guess + ch.encode()
                print(f"Length of Front Padding = {i} || Current Guess: {current_flag_guess}")
                i = i - 1
                break
