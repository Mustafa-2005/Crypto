import numpy as np

def caesar_cipher(text, shift, mode):
    result = "" 
    for char in text:
        if char.isalpha():
            shift_amount = shift if mode == "1" else -shift
            if char.islower():
                result += chr(((ord(char) - 97 + shift_amount) % 26) + 97)
            else:
                result += chr(((ord(char) - 65 + shift_amount) % 26) + 65)
        else:
            result += char
    return result


def vigenere_cipher(text, key, mode):
    result = ""
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            key_char = key[i % key_length]
            shift = ord(key_char.lower()) - 97
            shift_amount = shift if mode == "1" else -shift
            if char.islower():
                result += chr(((ord(char) - 97 + shift_amount) % 26) + 97)
            else:
                result += chr(((ord(char) - 65 + shift_amount) % 26) + 65)
        else:
            result += char
    return result

def monoalphabetic_encrypt(plaintext, key):
    """Encrypt a message using a monoalphabetic substitution cipher."""
    plaintext = plaintext.upper()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    translation_table = str.maketrans(alphabet, key)
    return plaintext.translate(translation_table)

def monoalphabetic_decrypt(ciphertext, key):
    """Decrypt a message using a monoalphabetic substitution cipher."""
    ciphertext = ciphertext.upper()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    translation_table = str.maketrans(key, alphabet)
    return ciphertext.translate(translation_table)

def create_playfair_matrix(keyword):
    """Generate a 5x5 Playfair cipher matrix."""
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    keyword = "".join(dict.fromkeys(keyword.upper().replace("J", "I")))  # Remove duplicates
    matrix_string = keyword + "".join(filter(lambda x: x not in keyword, alphabet))
    matrix = np.array(list(matrix_string)).reshape(5, 5)
    return matrix

def find_position(matrix, letter):
    """Find row and column of a letter in the Playfair matrix."""
    row, col = np.where(matrix == letter)
    return row[0], col[0]

def playfair_encrypt(text, matrix):
    """Encrypt text using Playfair cipher."""
    text = text.upper().replace("J", "I")
    text_pairs = []

    # Prepare digraphs
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else 'X'
        if a == b:
            text_pairs.append((a, 'X'))
            i += 1
        else:
            text_pairs.append((a, b))
            i += 2

    encrypted_text = []
    for a, b in text_pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:  # Same row
            encrypted_text.append(matrix[row1, (col1 + 1) % 5])
            encrypted_text.append(matrix[row2, (col2 + 1) % 5])
        elif col1 == col2:  # Same column
            encrypted_text.append(matrix[(row1 + 1) % 5, col1])
            encrypted_text.append(matrix[(row2 + 1) % 5, col2])
        else:  # Rectangle swap
            encrypted_text.append(matrix[row1, col2])
            encrypted_text.append(matrix[row2, col1])

    return "".join(encrypted_text)

def playfair_decrypt(ciphertext, matrix):
    """Decrypt text using Playfair cipher."""
    decrypted_text = []
    text_pairs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]

    for a, b in text_pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:  # Same row
            decrypted_text.append(matrix[row1, (col1 - 1) % 5])
            decrypted_text.append(matrix[row2, (col2 - 1) % 5])
        elif col1 == col2:  # Same column
            decrypted_text.append(matrix[(row1 - 1) % 5, col1])
            decrypted_text.append(matrix[(row2 - 1) % 5, col2])
        else:  # Rectangle swap
            decrypted_text.append(matrix[row1, col2])
            decrypted_text.append(matrix[row2, col1])

    return "".join(decrypted_text)




def rail_fence_encrypt(text, key):
    rail = [['\n' for _ in range(len(text))] for _ in range(key)]

    dir_down = False
    row, col = 0, 0

    for ch in text:
        if row == 0 or row == key - 1:
            dir_down = not dir_down

        rail[row][col] = ch
        col += 1
        row += 1 if dir_down else -1

    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return ''.join(result)

def rail_fence_decrypt(cipher, key):
    rail = [['\n' for _ in range(len(cipher))] for _ in range(key)]

    dir_down = None
    row, col = 0, 0

    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False

        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1

    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1

    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False

        if rail[row][col] != '\n':
            result.append(rail[row][col])
            col += 1

        row += 1 if dir_down else -1

    return ''.join(result)

def columnar_transposition_encrypt(plaintext, key):
    plaintext = plaintext.replace(" ", "").upper()
    key = key.upper()

    num_cols = len(key)
    num_rows = (len(plaintext) + num_cols - 1) // num_cols
    padding_len = num_rows * num_cols - len(plaintext)
    plaintext += 'X' * padding_len  # Pad with Xs

    # Create the matrix
    matrix = ['' for _ in range(num_rows)]
    for i in range(num_rows):
        matrix[i] = plaintext[i * num_cols : (i + 1) * num_cols]

    # Sort key with index
    order = sorted([(char, idx) for idx, char in enumerate(key)])
    col_order = [idx for (char, idx) in order]

    # Read columns in sorted key order
    ciphertext = ''
    for col in col_order:
        for row in matrix:
            ciphertext += row[col]

    return ciphertext


def columnar_transposition_decrypt(ciphertext, key):
    ciphertext = ciphertext.replace(" ", "").upper()
    key = key.upper()

    num_cols = len(key)
    num_rows = len(ciphertext) // num_cols

    # Sort key with index
    order = sorted([(char, idx) for idx, char in enumerate(key)])
    col_order = [idx for (char, idx) in order]

    # Fill columns based on sorted key order
    matrix = ['' for _ in range(num_cols)]
    k = 0
    for col in col_order:
        matrix[col] = ciphertext[k:k + num_rows]
        k += num_rows

    # Read matrix row-wise
    plaintext = ''
    for row in range(num_rows):
        for col in range(num_cols):
            plaintext += matrix[col][row]

    return plaintext


