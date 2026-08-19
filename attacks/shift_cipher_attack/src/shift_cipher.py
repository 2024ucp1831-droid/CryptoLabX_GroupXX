def encrypt(text, key):
    result = ""

    for char in text:
        if char.isupper():
            result += chr((ord(char) - ord('A') + key) % 26 + ord('A'))
        elif char.islower():
            result += chr((ord(char) - ord('a') + key) % 26 + ord('a'))
        else:
            result += char

    return result


def decrypt(text, key):
    return encrypt(text, -key)


if __name__ == "__main__":
    plaintext = input("Enter plaintext: ")
    key = int(input("Enter key: "))

    ciphertext = encrypt(plaintext, key)

    print("Ciphertext:", ciphertext)
    print("Decrypted:", decrypt(ciphertext, key))
