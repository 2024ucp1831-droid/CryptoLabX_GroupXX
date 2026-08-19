# brute_force_dictionary.py

import os
import sys

# Allow importing shift_cipher.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from shift_cipher import decrypt


def load_dictionary(dictionary_file):
    """
    Load English words from dictionary file.
    """

    words = set()

    try:
        with open(dictionary_file, "r", encoding="utf-8") as file:

            for line in file:
                word = line.strip().lower()

                if word:
                    words.add(word)

    except FileNotFoundError:
        print("Dictionary file not found!")
        return set()

    return words


def dictionary_score(text, dictionary):
    """
    Count how many words in the text
    are present in the dictionary.
    """

    words = text.lower().split()

    score = 0

    for word in words:

        # Remove punctuation
        cleaned_word = ""

        for char in word:
            if char.isalpha():
                cleaned_word += char

        if cleaned_word in dictionary:
            score += 1

    return score


def brute_force_dictionary(ciphertext, dictionary_file):

    dictionary = load_dictionary(dictionary_file)

    results = []

    for key in range(26):

        plaintext = decrypt(ciphertext, key)

        score = dictionary_score(
            plaintext,
            dictionary
        )

        results.append({
            "key": key,
            "plaintext": plaintext,
            "score": score
        })

    # Highest dictionary score
    best_result = max(
        results,
        key=lambda x: x["score"]
    )

    return best_result, results


if __name__ == "__main__":

    ciphertext = input("Enter ciphertext: ")

    dictionary_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "dictionary",
        "english_words.txt"
    )

    best, results = brute_force_dictionary(
        ciphertext,
        dictionary_file
    )

    print("\n===== DICTIONARY SCORING =====")

    for result in results:

        print(
            f"Key: {result['key']:2d} | "
            f"Score: {result['score']:3d} | "
            f"{result['plaintext']}"
        )

    print("\nBest Key:", best["key"])
    print("Best Score:", best["score"])
    print("Recovered Plaintext:", best["plaintext"])
