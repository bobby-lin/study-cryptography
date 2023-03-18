"""
Exercise: https://aes.cryptohack.org/flipping_cookie/
"""
from Crypto.Cipher import AES
import os
from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta


KEY = b'\xd1\x891\xb7\x1b\x0bM\xed\xc24\x1df\xed\x9a\xf9\x9d'
FLAG = 'crypto{wonderful_world!!!!!!!!!}'


def split_blocks(hex_data):
    block_size = 32
    split_arr = [hex_data[i:i + block_size] for i in range(0, len(hex_data), block_size)]
    return split_arr


def xor_bytes(b_1, b_2):
    return bytes(a ^ b for (a, b) in zip(b_1, b_2))


def brute_force_xor(cipher_text_byte, target_byte):
    # Bruteforce until we get the target_byte
    for c in range(0, 255):
        if target_byte == bytes([cipher_text_byte ^ c]):
            return c


def brute_force_iv(decrypted_list, iv_list):
    result = b''
    new_iv = b''

    for i in range(len(iv_list)):
        iv_byte = iv_list[i]

        if i == 6:
            iv_byte = brute_force_xor(decrypted_list[i], b'T')

        if i == 7:
            iv_byte = brute_force_xor(decrypted_list[i], b'r')

        if i == 8:
            iv_byte = brute_force_xor(decrypted_list[i], b'u')

        if i == 9:
            iv_byte = brute_force_xor(decrypted_list[i], b'e')

        if i == 10:
            iv_byte = brute_force_xor(decrypted_list[i], b';')

        result += bytes([iv_byte ^ decrypted_list[i]])
        new_iv += bytes([iv_byte])

    return result, new_iv


def check_admin(cookie, iv):
    cookie = bytes.fromhex(cookie)
    iv = bytes.fromhex(iv)

    try:
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(cookie)
        unpadded = unpad(decrypted, 16)
    except ValueError as e:
        return {"error": str(e)}
    if b"admin=True" in unpadded.split(b";"):
        return {"flag": FLAG}
    else:
        return {"error": "Only admin can read the flag"}


def encrypt(cookie, iv):
    padded = pad(cookie, 16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded)
    return encrypted


def get_cookie():
    expires_at = (datetime.today() + timedelta(days=1)).strftime("%S")
    cookie = f"admin=False;expiry={expires_at}".encode()
    iv = os.urandom(16)
    encrypted = encrypt(cookie, iv)
    ciphertext = iv.hex() + encrypted.hex()
    return {"cookie": ciphertext}


cookie_blocks = split_blocks(get_cookie()['cookie'])

iv = cookie_blocks[0]

cookie = ""
for i in range(1, len(cookie_blocks)):
    cookie += cookie_blocks[i]

"""
Let X be the decrypted value before ⊕ with IV
Let Y be the IV value
Let Z be the cookie value (b'admin=False;expi')
X ⊕ Y = Z
If we perform Y ⊕  Z, then we will get the decrypted value X before ⊕ with iv.
Using the decrypted value X, we can brute-force the iv Y value that gives us the value b'admin=True;;expi'
"""

bytes_1 = b'admin=False;expi'
bytes_2 = bytes.fromhex(iv)

# Get decrypted value before xor with iv
decrypted_block_1 = xor_bytes(bytes_1, bytes_2)
decrypted_block_1_list = list(decrypted_block_1)

# Bruteforce to find the new iv that gives use the cookie "admin=True;;expi"
result, new_iv = brute_force_iv(decrypted_block_1_list, list(bytes.fromhex(iv)))
print("New Cookie: ", result)
print("New IV: ", new_iv.hex())

print(check_admin(cookie, new_iv.hex()))
