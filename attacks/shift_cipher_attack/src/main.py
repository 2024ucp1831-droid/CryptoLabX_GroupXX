# main.py

import os

from shift_cipher import decrypt
from brute_force_dictionary import brute_force_dictionary
from chi_square_attack import chi_square_attack


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DICTIONARY_FILE = os.path.join(
    BASE_DIR,
    "dictionary",
    "english_words.txt"
)


def read_ciphertext():

    print("======================================")
    print(" SHIFT CIPHER CRYPTANALYSIS")
    print("======================================")

    print("\n1. Enter ciphertext manually")
    print("2. Read ciphertext from testcase file")

    choice = input("\nEnter choice: ")

    if choice == "1":

        return input(
            "\nEnter ciphertext: "
        )

    elif choice == "2":

        filename = input(
            "Enter testcase filename: "
        )

        filepath = os.path.join(
            BASE_DIR,
            "testcases",
            filename
        )

        try:

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                return file.read().strip()

        except FileNotFoundError:

            print("Testcase file not found!")

            return None

    else:

        print("Invalid choice.")

        return None


def save_results(
    ciphertext,
    dictionary_result,
    chi_result
):

    output_dir = os.path.join(
        BASE_DIR,
        "outputs"
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    output_file = os.path.join(
        output_dir,
        "results.txt"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "SHIFT CIPHER CRYPTANALYSIS RESULTS\n"
        )

        file.write(
            "====================================\n\n"
        )

        file.write(
            f"Ciphertext:\n{ciphertext}\n\n"
        )

        file.write(
            "DICTIONARY SCORING\n"
        )

        file.write(
            "------------------\n"
        )

        file.write(
            f"Predicted Key: "
            f"{dictionary_result['key']}\n"
        )

        file.write(
            f"Dictionary Score: "
            f"{dictionary_result['score']}\n"
        )

        file.write(
            f"Plaintext: "
            f"{dictionary_result['plaintext']}\n\n"
        )

        file.write(
            "CHI-SQUARE ANALYSIS\n"
        )

        file.write(
            "-------------------\n"
        )

        file.write(
            f"Predicted Key: "
            f"{chi_result['key']}\n"
        )

        file.write(
            f"Chi-Square Value: "
            f"{chi_result['chi_square']:.4f}\n"
        )

        file.write(
            f"Plaintext: "
            f"{chi_result['plaintext']}\n\n"
        )

        file.write(
            "COMPARISON\n"
        )

        file.write(
            "----------\n"
        )

        if (
            dictionary_result["key"]
            == chi_result["key"]
        ):

            file.write(
                "Both methods predicted "
                "the same key.\n"
            )

        else:

            file.write(
                "The two methods predicted "
                "different keys.\n"
            )

    print(
        f"\nResults saved to: {output_file}"
    )


def main():

    ciphertext = read_ciphertext()

    if ciphertext is None:
        return

    print("\nDecrypting using all 26 keys...\n")

    dictionary_best, dictionary_results = (
        brute_force_dictionary(
            ciphertext,
            DICTIONARY_FILE
        )
    )

    chi_best, chi_results = (
        chi_square_attack(ciphertext)
    )

    print("\n======================================")
    print(" DICTIONARY SCORING RESULT")
    print("======================================")

    print(
        "Predicted Key:",
        dictionary_best["key"]
    )

    print(
        "Dictionary Score:",
        dictionary_best["score"]
    )

    print(
        "Plaintext:",
        dictionary_best["plaintext"]
    )

    print("\n======================================")
    print(" CHI-SQUARE RESULT")
    print("======================================")

    print(
        "Predicted Key:",
        chi_best["key"]
    )

    print(
        "Chi-Square:",
        round(
            chi_best["chi_square"],
            4
        )
    )

    print(
        "Plaintext:",
        chi_best["plaintext"]
    )

    print("\n======================================")
    print(" COMPARISON")
    print("======================================")

    if (
        dictionary_best["key"]
        == chi_best["key"]
    ):

        print(
            "Both attacks predicted the SAME key."
        )

    else:

        print(
            "The attacks predicted DIFFERENT keys."
        )

    save_results(
        ciphertext,
        dictionary_best,
        chi_best
    )


if __name__ == "__main__":
    main()
