# Decrypting with known partial plaintext

Lab link: https://aes.cryptohack.org/bean_counter/

This is the source code provided by the lab. We can see that the encrypted image is a PNG format.
```python
from Crypto.Cipher import AES


KEY = ?


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



@chal.route('/bean_counter/encrypt/')
def encrypt():
    cipher = AES.new(KEY, AES.MODE_ECB)
    ctr = StepUpCounter()

    out = []
    with open("challenge_files/bean_flag.png", 'rb') as f:
        block = f.read(16)
        while block:
            keystream = cipher.encrypt(ctr.increment())
            xored = [a^b for a, b in zip(block, keystream)]
            out.append(bytes(xored).hex())
            block = f.read(16)

    return {"encrypted": ''.join(out)}
```
Another observation is that the encrypted value is the same value even if you try to call the endpoint multiple times.

Endpoint: https://aes.cryptohack.org/bean_counter/encrypt/

This means the Keystream is the same => Which means the IV will be the same static value.

```text
{"encrypted":"e98314052b369f82c90eab82d59...."}
```

We know this fact:

```text
KeyStream ⊕ PlainTextBlock[n] = CiperTextBlock[n]
```

## But how do we get the KeyStream given that we don't really know the entire plaintext block?

After thinking for a while, I noticed that every plaintext of a PNG image will start with the same block `b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'`.

Try printing out the first block (16) in three different PNG file.
```python
with open("bean_flag.png", 'rb') as f:
    block = f.read(16)
    print(block)

with open("bean_flag_2.png", 'rb') as f:
    block = f.read(16)
    print(block)

with open("dice.png", 'rb') as f:
    block = f.read(16)
    print(block)
```
You will see the PNG format header
```console
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
```
To get the KeyStream:
```text
PlainTextBlock[0] ⊕ CiperTextBlock[0]
= 'b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'' ⊕ CiperTextBlock[0]
= KeyStream
```
## Finally
To get the actual plaintext of all blocks:
```text
KeyStream ⊕ CiperTextBlock[n] = PlainTextBlock[n] 
```
Combine all the bytes and save it as a image file.