import matrix

"""
state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]

"""


def add_round_key(s, k):
    final_state = []
    for i in range(4):
        row_state = []
        for y in range(4):
            # Sn XOR Kn
            row_state.append(s[i][y] ^ k[i][y])

        final_state.append(row_state)
    return final_state


#print(add_round_key(state, round_key))
#print(matrix.matrix2bytes(add_round_key(state, round_key)))
