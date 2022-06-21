# Introduction to CryptoHack

## Encoding
### ASCII
- Represent text with integers between 0 - 127
- Use Python's `chr()` function to convert ASCII ordinal number to a character. `ord()` function convert char to ASCII nummber

### Hex
- Purpose: Usually the output of the encrypted data are in bytes and are not printable ASCII characters. 
- We can encode the encrypted data with hex format.
```python
>>> bytes.fromhex('63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d')
b'crypto{You_will_be_working_with_hex_strings_a_lot}'
```
- `bytes.fromhex(...)` convert hex -> bytes
- `[bytes].hex()`: byte strings -> hex
- https://docs.python.org/3/library/stdtypes.html?highlight=fromhe#bytes.fromhex

### Base64
- Represent binary data as ASCII string with 64 chars
- 1 char of Base64 string encodes 6 bits.
	- 4 chars of the base64 string will encode three 8-bits bytes.
	- 64 chars -> 396-bits bytes
- Common task: Decode a hex string into bytes and encode the bytes into base64.
- Use `base64.b64encode(...)`  to encode the bytes into base64 encoding format.

### Conversion between Bytes and Integer
- RSA works on numbers but most messages consist of characters.
- Very often, we need to convert our messages into numbers so that the encryption algorithm can work on the message.
- One common method is convert the ordinal bytes of the message into hexdecimal and concatenate them.
- PyCryptodome library can help to convert integers into bytes (`Crypto.Util.number.long_to_bytes()`) or bytes into integer (`Crypto.Util.number.bytes_to_long()`).

```Python
>>> from Crypto.Util.number import *
>>> long_to_bytes(11515195063862318899931685488813747395775516287289682636499965282714637259206269)
b'crypto{3nc0d1n6_4ll_7h3_w4y_d0wn}'
```

### XOR
- Used to mix the key and data together
- Represented as ⊕ or `^`
- A bitwise operator:
	- A ⊕ B
		- 1 ⊕ 1 = 0
		- 0 ⊕ 0 = 0
		- 1 ⊕ 0 = 1
		- 0 ⊕ 1 = 1
- Conversion scenarios:
	- integers
	- string
		- convert each character to integer that represent the unicode char
#### Problem
Given the string `"label"`, XOR each character with the integer `13`. Convert these integers back to a string and submit the flag as `crypto{new_string}`.

```Python
msg_int_arr = [ord(x) for x in "label"]
final_msg_arr = [chr(x ^ 13) for x in msg_integer]
print(''.join(final_msg_arr))
```

#### XOR Properties
```
KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313  
KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e  
KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1  
FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf
```
Remember to decode from hex to bytes before you XOR the objects.

```Python
from Crypto.Util.number import *

"""
KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf

Solution:
KEY2 ^ KEY1 ^ KEY1 = KEY2
KEY2 ^ KEY2 ^ KEY3 = KEY3
FLAG ^ KEY1 ^ KEY3 ^ KEY2 ^ KEY1 ^ KEY3 ^ KEY2 = FLAG
"""

part_1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
part_2 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
part_3 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
part_4 = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

key1_long = bytes_to_long(bytes.fromhex(part_1))
key2_long = key1_long ^ bytes_to_long(bytes.fromhex(part_2))
key3_long = key2_long ^ bytes_to_long(bytes.fromhex(part_3))
flag_long = bytes_to_long(bytes.fromhex(part_4)) ^ key3_long ^ key2_long ^ key1_long

print(long_to_bytes(flag_long))
```

### XOR Single Bytes - bruteforce

```Python
"""  
data ^ sb = 73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d  
where sb is a single byte  
"""  

def single_byte_xor(input, key):  
    output = b''  
    for b in input:  
        output += bytes([b ^ key])  
  
    return output


cipher_txt = bytes.fromhex("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")  
  
for i in range(1, 256):  
    decrypted = single_byte_xor(cipher_txt, i)  
    if b'crypto' in decrypted:
        print(decrypted)

```

### XOR (using known format attack)
An encryption that uses XOR only with the key is vulnerable to known format attack if we know the data format.

We know the format of the flag starts with `crypto{`.

```Python
"""
You either know, XOR you don't
flag ^ key = cipher_txt
1) Find the partial key?
partial cipher_txt ^ partial flag crypt{crypt{ = myXORke
>> The key should be myXORkey
"0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104" ⊕ "myXORkeymyXORkeymyXORkey..."
"""

cipher_txt = bytes.fromhex("0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104")
partial_flag = 'crypto{1'

key = ''.join([chr(cipher_txt[i] ^ ord(partial_flag[i])) for i in range(len(partial_flag))])

output = b''

# XOR the cipher text bit and key bit
# CipherText: 14 11 33 63 ...
#              ⊕ ⊕ ⊕ ⊕
#        Key: 109 121 88 79 ...
#       Flag: 99 (c) 114 (r)
for i in range(len(cipher_txt)):
  output += bytes([cipher_txt[i] ^ ord(key[i % len(key)])])

print(output)
```
