import requests
from Crypto.Cipher import AES
import os
import io

KEY = b'\xd1\x891\xb7\x1b\x0bM\xed\xc24\x1df\xed\x9a\xf9\x9d'


class StepUpCounter(object):
    def __init__(self, value=os.urandom(16), step_up=False):
        self.value = value.hex()
        self.step = 1
        self.stup = step_up

    def increment(self):
        if self.stup:
            self.newIV = hex(int(self.value, 16) + self.step)
        else:
            self.newIV = hex(int(self.value, 16) - self.stup)
        self.value = self.newIV[2:len(self.newIV)]
        return bytes.fromhex(self.value.zfill(32))

    def __repr__(self):
        self.increment()
        return self.value


def encrypt():
    cipher = AES.new(KEY, AES.MODE_ECB)
    ctr = StepUpCounter()

    out = []
    num = 1
    with open("challenge_files/bean_flag.png", 'rb') as f:
        block = f.read(16)
        while block:
            keystream = cipher.encrypt(ctr.increment())
            xored = [a^b for a, b in zip(block, keystream)]
            out.append(bytes(xored).hex())
            print(num, block, keystream, bytes(xored).hex())

            block = f.read(16)
            num += 1

    return {"encrypted": ''.join(out)}


def split_blocks(hex_data):
    block_size = 32
    split_arr = [hex_data[i:i + block_size] for i in range(0, len(hex_data), block_size)]
    return split_arr

def get_keystream(ciphertext, first_block_pt):
    out = []
    xored = get_xor_bytes(ciphertext, first_block_pt)
    out.append(bytes(xored).hex())
    return ''.join(out)


def get_encrypted_ct():
    url = "https://aes.cryptohack.org/bean_counter/encrypt/"
    return requests.get(url).json()['encrypted']

def get_xor_bytes(bytes_1, bytes_2):
    return [a ^ b for a, b in zip(bytes_1, bytes_2)]


# data = encrypt()
# print(len(data['encrypted']))
# cipher_blocks = split_blocks(data['encrypted'])


first_block_pt = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
data = get_encrypted_ct()
cipher_blocks = split_blocks(data)
ks = get_keystream(bytes.fromhex(cipher_blocks[0]), first_block_pt)

bytes_data_arr = []

for c in cipher_blocks:
    xor_bytes = get_xor_bytes(bytes.fromhex(c), bytes.fromhex(ks))
    bytes_data_arr.append(bytes(xor_bytes))


image_bytes = b''.join(bytes_data_arr)
with open('challenge_files/decrypted_bean_flag.png', 'wb') as file:
    file.write(image_bytes)

print("Generated decrypted img!")
