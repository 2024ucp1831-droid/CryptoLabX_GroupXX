# shift_cipher.py

def encrypt(text, key):
    """
    Encrypt text using Shift/Caesar Cipher.
    """

    result = ""

    for char in text:
        if char.isalpha():

            if char.isupper():
                result += chr((ord(char) - ord('A') + key) % 26 + ord('A'))

            else:
                result += chr((ord(char) - ord('a') + key) % 26 + ord('a'))

        else:
            result += char

    return result


def decrypt(text, key):
    """
    Decrypt text using Shift/Caesar Cipher.
    """

    return encrypt(text, -key)


if __name__ == "__main__":

    plaintext = input("Enter plaintext: ")
    key = int(input("Enter key (0-25): "))

    ciphertext = encrypt(plaintext, key)

    print("\nCiphertext:", ciphertext)

    decrypted = decrypt(ciphertext, key)

    print("Decrypted:", decrypted)
