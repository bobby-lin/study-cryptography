import os
from Crypto.Cipher import AES

KEY = b'\xd1\x891\xb7\x1b\x0bM\xed\xc24\x1df\xed\x9a\xf9\x9d'
FLAG = 'crypto{wonderful_world!!!!!!!!!}'


def decrypt(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)

    cipher = AES.new(KEY, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}


def encrypt_flag():
    iv = os.urandom(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(FLAG.encode())
    ciphertext = iv.hex() + encrypted.hex()

    return {"ciphertext": ciphertext}


def split_blocks(hex_data):
    block_size = 32
    split_arr = [hex_data[i:i + block_size] for i in range(0, len(hex_data), block_size)]
    return split_arr


def xor_bytes(hex_1, hex_2):
    return bytes(a ^ b for (a, b) in zip(bytes.fromhex(hex_1), bytes.fromhex(hex_2)))


ciphertext = encrypt_flag()['ciphertext']
ciphertext_arr = split_blocks(ciphertext)
print(ciphertext_arr)

# Decrypt second block (plaintext) and xor with the first block (IV)
first_block = decrypt(ciphertext_arr[1])['plaintext']
iv = ciphertext_arr[0]
first_block_xor_iv = xor_bytes(first_block, iv)  # First step of CBC decryption

second_block = decrypt(ciphertext_arr[2])['plaintext']
second_block_xor_first_block = xor_bytes(second_block, ciphertext_arr[1]) # Second step of CBC decryption

print(f"FLAG = {first_block_xor_iv}{second_block_xor_first_block}")