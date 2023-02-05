import matrix
import diffusion
from add_round_key import add_round_key
from sbox import s_box, inv_s_box, sub_bytes

N_ROUNDS = 10

key = b'\xc3,\\\xa6\xb5\x80^\x0c\xdb\x8d\xa5z*\xb6\xfe\\'
ciphertext = b'\xd1O\x14j\xa4+O\xb6\xa1\xc4\x08B)\x8f\x12\xdd'


def expand_key(master_key):
    """
    Expands and returns a list of key matrices for the given master_key.
    """

    # Round constants https://en.wikipedia.org/wiki/AES_key_schedule#Round_constants
    r_con = (
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
    )

    # Initialize round keys with raw key material.
    key_columns = matrix.bytes2matrix(master_key)
    iteration_size = len(master_key) // 4

    # Each iteration has exactly as many columns as the key material.
    i = 1
    while len(key_columns) < (N_ROUNDS + 1) * 4:
        # Copy previous word.
        word = list(key_columns[-1])

        # Perform schedule_core once every "row".
        if len(key_columns) % iteration_size == 0:
            # Circular shift.
            word.append(word.pop(0))
            # Map to S-BOX.
            word = [s_box[b] for b in word]
            # XOR with first byte of R-CON, since the others bytes of R-CON are 0.
            word[0] ^= r_con[i]
            i += 1
        elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
            # Run word through S-box in the fourth iteration when using a
            # 256-bit key.
            word = [s_box[b] for b in word]

        # XOR with equivalent word from previous iteration.
        word = bytes(i ^ j for i, j in zip(word, key_columns[-iteration_size]))
        key_columns.append(word)

    # Group key words in 4x4 byte matrices.
    return [key_columns[4 * i: 4 * (i + 1)] for i in range(len(key_columns) // 4)]


def convert_key_to_matrix(k):
    return matrix.bytes2matrix(matrix.matrix2bytes(k))


def decrypt(key, ciphertext):
    # Remember to start from the last round key and work backwards through them when decrypting
    round_keys = expand_key(key)

    # Convert ciphertext to state matrix
    state = matrix.bytes2matrix(ciphertext)

    # Initial add round key step
    state = add_round_key(state, convert_key_to_matrix(round_keys[10]))

    for i in range(N_ROUNDS - 1, 0, -1):
        state = diffusion.inv_shift_rows(state)
        state = sub_bytes(state, inv_s_box)
        state = add_round_key(state, convert_key_to_matrix(round_keys[i]))
        state = diffusion.inv_mix_columns(state)

    # Run final round (skips the InvMixColumns step)
    state = diffusion.inv_shift_rows(state)
    state = sub_bytes(state, inv_s_box)
    state = add_round_key(state, convert_key_to_matrix(round_keys[0]))

    # Convert state matrix to plaintext
    plaintext = matrix.matrix2bytes(state)

    return plaintext


print(decrypt(key, ciphertext))
