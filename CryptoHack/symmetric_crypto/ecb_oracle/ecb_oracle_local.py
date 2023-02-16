from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from binascii import hexlify as hexa
from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import string

BLOCK_SIZE = 16
KEY = urandom(16)
FLAG = "crypto{unknown_123_aieOqxxxxx}"


def split_msg_to_blocks(data):
    split = [hexa(data[i:i+BLOCK_SIZE]) for i in range(0, len(data), BLOCK_SIZE)]
    return b' '.join(split)


def encrypt(plaintext):
    plaintext = bytes.fromhex(plaintext)
    padded = pad(plaintext + FLAG.encode(), 16)
    cipher = AES.new(KEY, AES.MODE_ECB)
    try:
        encrypted = cipher.encrypt(padded)
    except ValueError as e:
        return {"error": str(e)}

    return {"ciphertext": encrypted.hex()}


def run_encryption(p):
    return encrypt(p.hex())


def guess(i, flag):
    plaintext = b'\x01' * i + flag
    c = run_encryption(plaintext)
    return split_msg_to_blocks(bytes.fromhex(c['ciphertext']))


cipher_list = []

for i in range(1, 33):
    plaintext = b'\x01' * i
    c = run_encryption(plaintext)
    cipher_list.append(split_msg_to_blocks(bytes.fromhex(c['ciphertext'])))
    print(f"Length of Front Padding = {len(plaintext)} || C = {split_msg_to_blocks(bytes.fromhex(c['ciphertext']))}")


current_flag_guess = b""
i = 31  # Testing 2 blocks (32 bytes)

while True:
    if i == 0 or b"}" in current_flag_guess:
        break
    for ch in string.printable:
        flag_guess = current_flag_guess + ch.encode()
        c = guess(i, flag_guess)
        for ct in cipher_list:
            if ct.startswith(c.split(b" ")[0] + b" " + c.split(b" ")[1]):
                current_flag_guess = current_flag_guess + ch.encode()
                print(i, current_flag_guess)
                i = i - 1
                break
