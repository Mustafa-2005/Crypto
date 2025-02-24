def caesar_cipher(text, shift, mode):
    result = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift if mode == "encrypt" else -shift
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
            shift_amount = shift if mode == "encrypt" else -shift
            if char.islower():
                result += chr(((ord(char) - 97 + shift_amount) % 26) + 97)
            else:
                result += chr(((ord(char) - 65 + shift_amount) % 26) + 65)
        else:
            result += char
    return result


def main():
    print("Welcome to the Cipher Program!")

    # Ask the user for encryption or decryption
    action = input("Do you want to encrypt or decrypt? (encrypt/decrypt): ").lower()
    if action not in ["encrypt", "decrypt"]:
        print("Invalid choice. Please type 'encrypt' or 'decrypt'.")
        return

    # Ask the user for the cipher type
    cipher_type = input("Do you want to use Caesar Cipher or Vigenère Cipher? (caesar/vigenere): ").lower()
    if cipher_type not in ["caesar", "vigenere"]:
        print("Invalid choice. Please type 'caesar' or 'vigenere'.")
        return

    # Get the text input
    text = input("Enter the text: ")

    # Perform the selected operation
    if cipher_type == "caesar":
        shift = int(input("Enter the shift value (e.g., 3): "))
        result = caesar_cipher(text, shift, action)
    elif cipher_type == "vigenere":
        key = input("Enter the key: ")
        result = vigenere_cipher(text, key, action)

    # Display the result
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
