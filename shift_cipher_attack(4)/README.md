# Shift Cipher Cryptanalysis

## Lab Assignment 4

This project implements the cryptanalysis of a **Shift Cipher (Caesar Cipher)** using two different techniques:

1. **Brute Force with Dictionary Scoring**
2. **Chi-Square Frequency Analysis**

The purpose of the experiment is to recover the encryption key and plaintext without knowing the original key.

---

## 📁 Project Structure

```text
shift_cipher_attack/
│
├── src/
│   ├── shift_cipher.py
│   ├── brute_force_dictionary.py
│   ├── chi_square_attack.py
│   └── main.py
│
├── dictionary/
│   └── english_words.txt
│
├── testcases/
│   ├── testcase1.txt
│   └── testcase2.txt
│
├── outputs/
│   └── results.txt
│
├── screenshots/
│
├── reports/
│   └── Assignment_4_Report.pdf
│
└── README.md
```

---

## 🔐 Shift Cipher

The Shift Cipher encrypts each alphabetic character by shifting it by a fixed number of positions.

### Encryption

```text
C = (P + K) mod 26
```

### Decryption

```text
P = (C - K) mod 26
```

Where:

* `P` = Plaintext
* `C` = Ciphertext
* `K` = Encryption key

For example, with key `3`:

```text
Plaintext  : HELLO
Ciphertext : KHOOR
```

---

# 🔎 Cryptanalysis Techniques

## 1. Brute Force + Dictionary Scoring

The program tries all possible keys from `0` to `25`.

For every key:

1. The ciphertext is decrypted.
2. The resulting text is split into words.
3. Each word is checked against the English dictionary.
4. A score is calculated based on the number of valid English words.
5. The key with the highest score is selected.

### Example

```text
Ciphertext:
KHOOR ZRUOG

Key 3:
HELLO WORLD

Dictionary Score:
2
```

Therefore:

```text
Predicted Key = 3
```

---

## 2. Chi-Square Analysis

Chi-Square analysis uses the frequency distribution of English letters.

For every possible key:

1. The ciphertext is decrypted.
2. Letter frequencies are calculated.
3. The frequencies are compared with standard English frequencies.
4. A Chi-Square value is calculated.
5. The key with the **lowest Chi-Square value** is selected.

The formula used is:

```text
χ² = Σ ((Observed - Expected)² / Expected)
```

A lower Chi-Square value indicates that the decrypted text is statistically closer to normal English.

---

# ▶️ How to Run

Make sure Python 3 is installed.

Check Python:

```bash
python3 --version
```

Navigate to the project directory:

```bash
cd shift_cipher_attack
```

Run the main program:

```bash
python3 src/main.py
```

---

## 🖥️ Program Options

The program provides two options:

```text
======================================
 SHIFT CIPHER CRYPTANALYSIS
======================================

1. Enter ciphertext manually
2. Read ciphertext from testcase file
```

### Option 1 – Manual Input

Enter:

```text
1
```

Then provide the ciphertext:

```text
KHOOR ZRUOG
```

The program will perform both attacks.

---

### Option 2 – Test Case File

Enter:

```text
2
```

Then enter the testcase filename:

```text
testcase1.txt
```

The program reads the ciphertext from:

```text
testcases/testcase1.txt
```

---

# 📊 Results

The program displays:

* Dictionary predicted key
* Dictionary score
* Dictionary recovered plaintext
* Chi-Square predicted key
* Chi-Square value
* Chi-Square recovered plaintext
* Comparison between both attacks

Example:

```text
======================================
 DICTIONARY SCORING RESULT
======================================

Predicted Key: 3
Dictionary Score: 2
Plaintext: HELLO WORLD


======================================
 CHI-SQUARE RESULT
======================================

Predicted Key: 3
Plaintext: HELLO WORLD


======================================
 COMPARISON
======================================

Both attacks predicted the SAME key.
```

Results are also saved automatically to:

```text
outputs/results.txt
```

---

# 🧪 Test Cases

The project uses multiple test cases with different encryption keys.

A results table is maintained in the following format:

| Test Case   | Actual Key | Dictionary Key | Chi-Square Key | Dictionary Correct? | Chi-Square Correct? |
| ----------- | ---------: | -------------: | -------------: | ------------------- | ------------------- |
| Test Case 1 |          3 |              3 |              3 | Yes                 | Yes                 |
| Test Case 2 |          7 |              7 |              7 | Yes                 | Yes                 |
| Test Case 3 |         13 |             13 |             13 | Yes                 | Yes                 |
| Test Case 4 |          5 |              5 |              8 | Yes                 | No                  |
| Test Case 5 |         19 |             19 |             19 | Yes                 | Yes                 |

The actual results should be recorded based on the output of the program.

---

# ⚠️ Failure Analysis

Both techniques may fail under certain conditions.

### Dictionary Scoring

Dictionary scoring can fail when:

* The ciphertext is very short.
* The plaintext contains uncommon words.
* The dictionary does not contain certain words.
* The plaintext contains names or technical terms.

### Chi-Square Analysis

Chi-Square analysis can fail when:

* The ciphertext is very short.
* There are not enough letters for reliable frequency analysis.
* The plaintext does not follow normal English letter frequencies.
* The text contains many unusual words.

### Possible Improvements

The attacks can be improved by:

* Using a larger English dictionary.
* Using word-frequency scoring.
* Using longer ciphertexts.
* Using n-gram frequency analysis.
* Combining dictionary and statistical scores.

---

# 📌 Observations

1. Shift Cipher has only 26 possible keys.
2. Therefore, brute-force cryptanalysis is computationally easy.
3. Dictionary scoring works well when the plaintext contains common English words.
4. Chi-Square analysis works better with longer ciphertexts.
5. Short ciphertexts can produce unreliable frequency statistics.
6. Combining multiple scoring techniques can improve confidence in the recovered key.

---

# 🎯 Conclusion

This experiment demonstrates that the Shift Cipher is vulnerable to cryptanalysis because of its very small key space.

The **Dictionary Scoring** technique uses valid English words to identify the most likely plaintext, while **Chi-Square Analysis** uses the statistical frequency distribution of English letters.

By testing all 26 possible keys, the encryption key can often be recovered without any prior knowledge of the original key.

---

## 👨‍💻 Technologies Used

* Python 3
* Shift/Caesar Cipher
* Brute Force Cryptanalysis
* Dictionary Scoring
* Chi-Square Analysis
* Git & GitHub

---

## 📚 Lab Assignment

**Assignment:** Lab Assignment 4
**Topic:** Cryptanalysis of Shift Cipher using Brute Force, Dictionary Scoring and Chi-Square Analysis
