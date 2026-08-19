import os
import re
from shift_cipher import decrypt

DICTIONARY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dictionary",
    "english_words.txt"
)


def load_dictionary():
    with open(DICTIONARY_FILE, "r") as file:
        return set(word.strip().lower() for word in file)


def score_text(text, dictionary):
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return sum(1 for word in words if word in dictionary)


def dictionary_attack(ciphertext):
    dictionary = load_dictionary()

    best_key = 0
    best_score = -1
    best_plaintext = ""

    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        score = score_text(plaintext, dictionary)

        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, best_score


if __name__ == "__main__":
    ciphertext = input("Enter ciphertext: ")

    key, plaintext, score = dictionary_attack(ciphertext)

    print("Predicted Key:", key)
    print("Plaintext:", plaintext)
    print("Dictionary Score:", score)
