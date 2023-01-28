"""
Source: Serious Cryptography (Amusson 2018, pg 66 - 67)
Note: Code snippet is updated to Python3

Output:
key = b'5f9f3e3d4056e1f6fd1472ec0871ce91'
enc(b'00000000000000000000000000000000 00000000000000000000000000000000') = b'ec8ecc73666b9912f4179da0ab0bfebe ec8ecc73666b9912f4179da0ab0bfebe'

Notice that for the same plaintext, the same ciphertexts are returned. This is insecure!
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from binascii import hexlify as hex
from os import urandom

BLOCK_SIZE = 16


def display_as_blocks(data):
    split = [hex(data[i:i + BLOCK_SIZE]) for i in range(0, len(data), BLOCK_SIZE)]
    return b' '.join(split)


k = urandom(16)
print(f"key = {hex(k)}")

# Create an instance of AES-128 to encrypt and decrypt
cipher = Cipher(algorithm=algorithms.AES(k), mode=modes.ECB(), backend=default_backend())
aes_encrypt = cipher.encryptor()

# Generate 32-bytes of message
p = b'\x00' * BLOCK_SIZE * 2

c = aes_encrypt.update(p) + aes_encrypt.finalize()
print(f"enc({display_as_blocks(p)}) = {display_as_blocks(c)}")
