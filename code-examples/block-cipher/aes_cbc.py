"""
Source: Serious Cryptography (Amusson 2018, pg 68)
Note: Code snippet is updated to Python3
Output:
key = b'61e3cadb38693a2cb8e634d764c9cd69'
=================================================
iv = b'e935d1abdeae5075febe87cb72ef0bf0'
enc(b'00000000000000000000000000000000 00000000000000000000000000000000') = b'4b2716cdc7d5e5f8fc5790b4069f7130 c8bb4114b83eba6a130df1c48f617714'
=================================================
Encrypting the same p with same iv from previous step...
iv = b'e935d1abdeae5075febe87cb72ef0bf0'
enc(b'00000000000000000000000000000000 00000000000000000000000000000000') = b'4b2716cdc7d5e5f8fc5790b4069f7130 c8bb4114b83eba6a130df1c48f617714'
=================================================
Generating new iv and encrypting the same p...
iv = b'7a431321cf56fb549ceaba9355144100'
enc(b'00000000000000000000000000000000 00000000000000000000000000000000') = b'bbaced2a868fda2802bc60ad13603154 a019ae69acd8e276e7f2dc571fceee46'
Notes:
We can see that usage of different iv values will produce different c even if p is the same
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from binascii import hexlify as hexa
from os import urandom

BLOCK_SIZE = 16


def print_enc_info(p, c):
    print(f"enc({split_msg_to_blocks(p)}) = {split_msg_to_blocks(c)}")


def split_msg_to_blocks(data):
    split = [hexa(data[i:i+BLOCK_SIZE]) for i in range(0, len(data), BLOCK_SIZE)]
    return b' '.join(split)


k = urandom(16)
print(f"key = {hexa(k)}")
print("=================================================")

iv = urandom(16)
print(f"iv = {hexa(iv)}")

aes = Cipher(algorithm=algorithms.AES(k), mode=modes.CBC(iv), backend=default_backend())
aes_encryptor = aes.encryptor()

p = b'\x00' * BLOCK_SIZE * 2
c = aes_encryptor.update(p) + aes_encryptor.finalize()
print_enc_info(p, c)

print("=================================================")
print("Encrypting the same p with same iv from previous step...")
print(f"iv = {hexa(iv)}")
aes = Cipher(algorithm=algorithms.AES(k), mode=modes.CBC(iv), backend=default_backend())
aes_encryptor = aes.encryptor()
c = aes_encryptor.update(p) + aes_encryptor.finalize()
print_enc_info(p, c)


print("=================================================")
print("Generating new iv and encrypting the same p...")
iv = urandom(16)
print(f"iv = {hexa(iv)}")
aes = Cipher(algorithm=algorithms.AES(k), mode=modes.CBC(iv), backend=default_backend())
aes_encryptor = aes.encryptor()
c = aes_encryptor.update(p) + aes_encryptor.finalize()
print_enc_info(p, c)
