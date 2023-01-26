"""
Source: Serious Cryptography (Amusson 2018, pg 62)
Note: Code snippet is updated to Python3
Output Example:
key = b'cdeec4440c0914cec5dc9d29ac0d0485'
plaintext = b'01010101010101010101010101010101'
ciphertext = b'85efcebdfb18f6c2401d0478802e9f61'
decrypted plaintext = b'01010101010101010101010101010101'
"""
# Docs: https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from binascii import hexlify as hexa
from os import urandom

# Create a random 16-byte key with Python's crypto PRNG
k = urandom(16)
print(f"key = {hexa(k)}")

cipher = Cipher(algorithm=algorithms.AES(k), mode=modes.ECB(), backend=default_backend())
aes_encrypt = cipher.encryptor()

p = b'\x01' * 16
print(f"plaintext = {hexa(p)}")

c = aes_encrypt.update(p) + aes_encrypt.finalize()
print(f"ciphertext = {hexa(c)}")

aes_decrypt = cipher.decryptor()
dp = aes_decrypt.update(c) + aes_decrypt.finalize()
print(f"decrypted plaintext = {hexa(dp)}")
