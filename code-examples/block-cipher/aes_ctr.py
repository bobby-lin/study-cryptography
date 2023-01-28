"""
Source: Serious Cryptography (Amusson 2018, pg 71 - 72)
Note: Code snippet is updated to Python3

Output:
key = b'256225cca998d576f24567cfe0e84f46'
nonce = 3629397281598310158
enc(b'000102') = b'7a0cd0'
decrypt(b'7a0cd0') = b'000102'

Notes:
Use same nonce for the same message.
But different nonce for different message
Decryption is just encrypting the ciphertext
"""

from Crypto.Cipher import AES
from Crypto.Util import Counter
from binascii import hexlify as hexa
from os import urandom
from struct import unpack

k = urandom(16)
print(f"key = {hexa(k)}")

# See: https://docs.python.org/3/library/struct.html
# nonce is little-endian (<) unsigned long long (Q)
nonce = unpack('<Q', urandom(8))[0]
print(f"nonce = {nonce}")

# Instatiate a counter function
ctr = Counter.new(128, initial_value=nonce)

# Create an instance of AES in CTR mode and use ctr as counter
aes = AES.new(k, AES.MODE_CTR, counter=ctr)

# p does not need to be multiple of the block size now
p = b'\x00\x01\x02'

c = aes.encrypt(p)
print(f"enc({hexa(p)}) = {hexa(c)}")

# Decryption using the encrypt function
ctr = Counter.new(128, initial_value=nonce)
aes = AES.new(k, AES.MODE_CTR, counter=ctr)
p = aes.encrypt(c)
print(f"decrypt({hexa(c)}) = {hexa(p)}")
