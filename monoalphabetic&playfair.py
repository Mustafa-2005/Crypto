import itertools
import string
import collections

### SECTION 1: MONOALPHABETIC CIPHER ###

# Monoalphabetic Cipher Encryption & Decryption
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

# Given key from the worksheet
plaintext_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ciphertext_alphabet = "JITUAXYCEKBLNFRQVZMHOGSPWD"

# Example: Encrypt & Decrypt
message = "I LOVE CRYPTO"
encrypted_message = monoalphabetic_encrypt(message, ciphertext_alphabet)
decrypted_message = monoalphabetic_decrypt("JLAP FJHERFJL OFE", ciphertext_alphabet)

print(f"Encrypted: {encrypted_message}")
print(f"Decrypted: {decrypted_message}")

### BRUTE FORCE ATTACK ###
def brute_force_monoalphabetic(ciphertext, max_attempts=1000, stop_after=5):
    """Attempts to brute-force decrypt a monoalphabetic cipher."""
    alphabet = string.ascii_lowercase
    attempts = 0
    valid_decryptions = 0

    for perm in itertools.permutations(alphabet):
        key = ''.join(perm)
        decrypted_text = monoalphabetic_decrypt(ciphertext, key.upper())

        # Check if the decryption contains common words
        words = decrypted_text.lower().split()
        common_words = {"the", "be", "to", "of", "and", "a", "in", "that", "have", "i"}
        valid_words = sum(1 for word in words if word in common_words)

        if valid_words > 2:  # If at least 2 common words exist
            print(f"Possible decryption:\n{decrypted_text}\nUsing key: {key.upper()}\n")
            valid_decryptions += 1

        attempts += 1
        if attempts >= max_attempts or valid_decryptions >= stop_after:
            break

### FREQUENCY ANALYSIS ###
ENGLISH_FREQ = "etaoinshrdlcumwfgypbvkjxqz"

def frequency_analysis(ciphertext):
    """Performs frequency analysis on a ciphertext."""
    ciphertext = ciphertext.lower()
    letter_counts = collections.Counter(c for c in ciphertext if c.isalpha())
    sorted_letters = [pair[0] for pair in letter_counts.most_common()]

    # Map highest frequencies to English letter frequency
    mapping = {}
    for i, cipher_letter in enumerate(sorted_letters):
        if i < len(ENGLISH_FREQ):
            mapping[cipher_letter] = ENGLISH_FREQ[i]

    decrypted_text = "".join(mapping.get(char, char) for char in ciphertext)
    print("Possible decryption (based on frequency analysis):")
    print(decrypted_text)

# Example usage:
ciphertext = "YVCCF NFICU"
frequency_analysis(ciphertext)

### SECTION 2: PLAYFAIR CIPHER ###

import numpy as np

def generate_playfair_matrix(keyword):
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

# Example Playfair usage
keyword = "ORCHID"
matrix = generate_playfair_matrix(keyword)
print("Playfair Matrix:")
print(matrix)

plaintext = "HIKE THE FOOTHILLS"
ciphertext = playfair_encrypt(plaintext.replace(" ", ""), matrix)
print(f"Encrypted Playfair Text: {ciphertext}")

decrypted_text = playfair_decrypt("ILMILDRKRY", generate_playfair_matrix("LARKSPUR"))
print(f"Decrypted Playfair Text: {decrypted_text}")
