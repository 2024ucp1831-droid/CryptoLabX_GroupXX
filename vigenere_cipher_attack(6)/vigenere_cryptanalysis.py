from collections import Counter, defaultdict
from math import gcd


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def clean_ciphertext(ciphertext):
    return "".join(c for c in ciphertext.upper() if c.isalpha())


def find_repeated_patterns(ciphertext, min_length=3, max_length=5):
    patterns = defaultdict(list)

    for length in range(min_length, max_length + 1):
        for i in range(len(ciphertext) - length + 1):
            pattern = ciphertext[i:i + length]
            patterns[pattern].append(i)

    return {
        pattern: positions
        for pattern, positions in patterns.items()
        if len(positions) > 1
    }


def calculate_distances(repeated_patterns):
    distances = []

    for positions in repeated_patterns.values():
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                distances.append(positions[j] - positions[i])

    return distances


def find_factors(number, max_factor=50):
    factors = []

    for i in range(2, min(number, max_factor) + 1):
        if number % i == 0:
            factors.append(i)

    return factors


def kasiski_analysis(ciphertext):
    repeated_patterns = find_repeated_patterns(ciphertext)
    distances = calculate_distances(repeated_patterns)

    factor_counts = Counter()

    for distance in distances:
        for factor in find_factors(distance):
            factor_counts[factor] += 1

    candidates = factor_counts.most_common()

    return candidates, repeated_patterns, distances


def calculate_ic(text):
    n = len(text)

    if n <= 1:
        return 0.0

    counts = Counter(text)

    numerator = sum(count * (count - 1) for count in counts.values())
    denominator = n * (n - 1)

    return numerator / denominator


def split_into_groups(ciphertext, key_length):
    groups = [""] * key_length

    for i, char in enumerate(ciphertext):
        groups[i % key_length] += char

    return groups


def frequency_analysis(group):
    counts = Counter(group)
    total = len(group)

    table = {}

    for letter in ALPHABET:
        table[letter] = {
            "count": counts.get(letter, 0),
            "frequency": counts.get(letter, 0) / total if total else 0
        }

    return table


def find_shift(group):
    """
    Estimate Caesar shift using chi-squared frequency analysis.
    English expected frequencies are used.
    """

    english_freq = {
        "A": 0.08167, "B": 0.01492, "C": 0.02782,
        "D": 0.04253, "E": 0.12702, "F": 0.02228,
        "G": 0.02015, "H": 0.06094, "I": 0.06966,
        "J": 0.00153, "K": 0.00772, "L": 0.04025,
        "M": 0.02406, "N": 0.06749, "O": 0.07507,
        "P": 0.01929, "Q": 0.00095, "R": 0.05987,
        "S": 0.06327, "T": 0.09056, "U": 0.02758,
        "V": 0.00978, "W": 0.02360, "X": 0.00150,
        "Y": 0.01974, "Z": 0.00074
    }

    n = len(group)

    if n == 0:
        return 0

    counts = Counter(group)
    best_shift = 0
    best_score = float("inf")

    for shift in range(26):
        chi_square = 0

        for i, letter in enumerate(ALPHABET):
            cipher_index = (i + shift) % 26
            cipher_letter = ALPHABET[cipher_index]

            observed = counts.get(cipher_letter, 0)
            expected = english_freq[letter] * n

            if expected > 0:
                chi_square += ((observed - expected) ** 2) / expected

        if chi_square < best_score:
            best_score = chi_square
            best_shift = shift

    return best_shift


def find_key(groups):
    shifts = []

    for group in groups:
        shift = find_shift(group)
        shifts.append(shift)

    return "".join(ALPHABET[shift] for shift in shifts)


def vigenere_decrypt(ciphertext, key):
    plaintext = []
    key = clean_ciphertext(key)

    for i, char in enumerate(ciphertext):
        cipher_value = ord(char) - ord("A")
        key_value = ord(key[i % len(key)]) - ord("A")

        plain_value = (cipher_value - key_value) % 26
        plaintext.append(chr(plain_value + ord("A")))

    return "".join(plaintext)


def vigenere_encrypt(plaintext, key):
    ciphertext = []
    key = clean_ciphertext(key)

    for i, char in enumerate(plaintext):
        plain_value = ord(char) - ord("A")
        key_value = ord(key[i % len(key)]) - ord("A")

        cipher_value = (plain_value + key_value) % 26
        ciphertext.append(chr(cipher_value + ord("A")))

    return "".join(ciphertext)


def verify(original_ciphertext, plaintext, key):
    encrypted = vigenere_encrypt(plaintext, key)

    return encrypted == original_ciphertext


def select_key_length(ciphertext, candidates):
    """
    Select a likely key length using Kasiski candidates and average IC.
    """

    if not candidates:
        return 1

    # Try top Kasiski candidates.
    candidate_lengths = [length for length, _ in candidates if 1 < length <= 20]

    if not candidate_lengths:
        candidate_lengths = list(range(2, 13))

    best_length = candidate_lengths[0]
    best_score = float("-inf")

    for length in candidate_lengths:
        groups = split_into_groups(ciphertext, length)

        ics = [
            calculate_ic(group)
            for group in groups
            if len(group) > 1
        ]

        if not ics:
            continue

        average_ic = sum(ics) / len(ics)

        # English-like text generally has IC around 0.065.
        score = -abs(average_ic - 0.065)

        # Give Kasiski ranking a small bonus.
        for rank, candidate in enumerate(candidate_lengths):
            if candidate == length:
                score += max(0, 0.01 - rank * 0.0005)
                break

        if score > best_score:
            best_score = score
            best_length = length

    return best_length


def print_frequency_table(groups):
    for index, group in enumerate(groups, start=1):
        print(f"\nGroup {index}: {group}")
        table = frequency_analysis(group)

        print("Letter  Count  Frequency")

        for letter in ALPHABET:
            count = table[letter]["count"]
            frequency = table[letter]["frequency"]

            print(f"{letter:>6}  {count:>5}  {frequency:.4f}")


def run_vigenere_attack(filename="datasets/vigenere_ciphertext.txt"):
    print("\n========== VIGENERE CRYPTANALYSIS ==========")

    with open(filename, "r") as file:
        raw_ciphertext = file.read()

    ciphertext = clean_ciphertext(raw_ciphertext)

    print("\n[1] Preprocessed Ciphertext")
    print(f"Ciphertext length: {len(ciphertext)}")
    print(ciphertext)

    print("\n[2] Kasiski Examination")

    candidates, repeated_patterns, distances = kasiski_analysis(ciphertext)

    print("Repeated patterns:")

    shown = 0
    for pattern, positions in repeated_patterns.items():
        print(f"{pattern}: {positions}")
        shown += 1

        if shown >= 15:
            break

    print("\nDistances:")
    print(distances)

    print("\nCandidate key lengths:")
    for length, count in candidates[:10]:
        print(f"Length {length}: {count} occurrences")

    key_length = select_key_length(ciphertext, candidates)

    print(f"\nEstimated key length: {key_length}")

    print("\n[3] Index of Coincidence")

    groups = split_into_groups(ciphertext, key_length)

    ic_values = []

    for i, group in enumerate(groups, start=1):
        ic = calculate_ic(group)
        ic_values.append(ic)
        print(f"Group {i} IC = {ic:.4f}")

    if ic_values:
        print(f"Average IC = {sum(ic_values) / len(ic_values):.4f}")

    print("\n[4] Frequency Analysis")

    print_frequency_table(groups)

    print("\n[5] Recovering Key")

    key = find_key(groups)

    print(f"Recovered key: {key}")

    print("\n[6] Decrypting")

    plaintext = vigenere_decrypt(ciphertext, key)

    print("Recovered plaintext:")
    print(plaintext)

    print("\n[7] Verification")

    result = verify(ciphertext, plaintext, key)

    if result:
        print("PASS: Re-encrypted ciphertext matches original ciphertext.")
    else:
        print("FAIL: Re-encrypted ciphertext does NOT match original ciphertext.")

    print("\n=============================================")

    return key, plaintext, result


if __name__ == "__main__":
    run_vigenere_attack()
