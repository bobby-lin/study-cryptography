import hashlib

from Crypto.Cipher import AES


def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    try:
        print(bytes.fromhex(decrypted.hex()).decode('ascii'))
    except:
        pass


# Get ciphertext from https://aes.cryptohack.org/passwords_as_keys/
ciphertext = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"

# /usr/share/dict/words from
# https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words
with open("wordlists/common_wordlist") as f:
    words = [w.strip() for w in f.readlines()]
    for keyword in words:
        try:
            password_hash = hashlib.md5(keyword.encode()).digest()
            decrypt(ciphertext, password_hash.hex())
        except:
            continue
