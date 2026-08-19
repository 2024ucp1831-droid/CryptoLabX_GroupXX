# chi_square_attack.py

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from shift_cipher import decrypt


# Standard English letter frequencies
ENGLISH_FREQUENCIES = {
    'a': 0.08167,
    'b': 0.01492,
    'c': 0.02782,
    'd': 0.04253,
    'e': 0.12702,
    'f': 0.02228,
    'g': 0.02015,
    'h': 0.06094,
    'i': 0.06966,
    'j': 0.00153,
    'k': 0.00772,
    'l': 0.04025,
    'm': 0.02406,
    'n': 0.06749,
    'o': 0.07507,
    'p': 0.01929,
    'q': 0.00095,
    'r': 0.05987,
    's': 0.06327,
    't': 0.09056,
    'u': 0.02758,
    'v': 0.00978,
    'w': 0.02360,
    'x': 0.00150,
    'y': 0.01974,
    'z': 0.00074
}


def calculate_letter_counts(text):

    counts = {}

    for letter in ENGLISH_FREQUENCIES:
        counts[letter] = 0

    for char in text.lower():

        if char in counts:
            counts[char] += 1

    return counts


def chi_square_score(text):

    counts = calculate_letter_counts(text)

    total_letters = sum(counts.values())

    if total_letters == 0:
        return float("inf")

    chi_square = 0

    for letter in ENGLISH_FREQUENCIES:

        observed = counts[letter]

        expected = (
            ENGLISH_FREQUENCIES[letter]
            * total_letters
        )

        if expected > 0:

            chi_square += (
                (observed - expected) ** 2
            ) / expected

    return chi_square


def chi_square_attack(ciphertext):

    results = []

    for key in range(26):

        plaintext = decrypt(ciphertext, key)

        score = chi_square_score(plaintext)

        results.append({
            "key": key,
            "plaintext": plaintext,
            "chi_square": score
        })

    # Lowest chi-square is best
    best_result = min(
        results,
        key=lambda x: x["chi_square"]
    )

    return best_result, results


if __name__ == "__main__":

    ciphertext = input("Enter ciphertext: ")

    best, results = chi_square_attack(ciphertext)

    print("\n===== CHI-SQUARE ANALYSIS =====")

    for result in results:

        print(
            f"Key: {result['key']:2d} | "
            f"Chi-Square: {result['chi_square']:.2f} | "
            f"{result['plaintext']}"
        )

    print("\nBest Key:", best["key"])

    print(
        "Chi-Square:",
        round(best["chi_square"], 2)
    )

    print(
        "Recovered Plaintext:",
        best["plaintext"]
    )
