Playfair Cipher in C++

A C++ implementation of the Playfair Cipher encryption and decryption algorithm.

This program generates a 5×5 Playfair key matrix, preprocesses the plaintext, creates digraphs, encrypts and decrypts messages, performs digraph frequency analysis, and verifies the encryption/decryption process.

Features

Generate a 5×5 Playfair key matrix

Convert J to I

Remove spaces and special characters

Handle repeated letters by inserting X

Handle odd-length plaintext

Encrypt plaintext using Playfair Cipher rules

Decrypt ciphertext

Perform digraph frequency analysis

Verify the result by re-encrypting the decrypted text

Requirements

Linux, macOS, or Windows

C++ compiler with C++11 or later

g++ recommended for Linux

Files
playfair.cpp
README.md

Compilation

Open a terminal in the project directory and run:

g++ playfair.cpp -o playfair

Running the Program

After compilation, run:

./playfair

Example Input
Keyword: MONARCHY
Plaintext: INSTRUMENTS

Key Matrix

For the keyword MONARCHY, the generated matrix is:

M O N A R
C H Y B D
E F G I K
L P Q S T
U V W X Z

Prepared Digraphs

The plaintext:

INSTRUMENTS


is divided into:

IN ST RU ME NT SX


The final X is padding because the plaintext has an odd number of characters.

Example Output
Key Matrix
M O N A R
C H Y B D
E F G I K
L P Q S T
U V W X Z

Prepared Digraphs:
IN ST RU ME NT SX

Ciphertext:
GATLMZCLRQXA

Decrypted Text:
INSTRUMENTSX

Digraph Frequency Analysis:
CL: 1
GA: 1
MZ: 1
RQ: 1
TL: 1
XA: 1

Verification:
SUCCESS

Playfair Cipher Rules

Each pair of letters is encrypted according to one of three rules.

1. Same Row

If both letters are in the same row, replace each letter with the letter immediately to its right.

The row wraps around from the last column to the first.

2. Same Column

If both letters are in the same column, replace each letter with the letter immediately below it.

The column wraps around from the last row to the first.

3. Rectangle Rule

If the letters are in different rows and columns, form a rectangle using their positions.

Each letter is replaced by the letter in the same row but the other letter's column.

Plaintext Processing

The program performs the following preprocessing:

Converts letters to uppercase.

Removes spaces and special characters.

Converts J to I.

Splits the plaintext into pairs.

Inserts X between repeated letters.

Adds X at the end if the plaintext has an odd number of characters.

For example:

BALLOON


is processed into:

BA LX LO ON

Verification

The program verifies the result by:

Plaintext
    ↓
Encryption
    ↓
Ciphertext
    ↓
Decryption
    ↓
Re-encryption
    ↓
Compare with original ciphertext


If both ciphertexts match, the program displays:

Verification:
SUCCESS


Otherwise:

Verification:
FAILED

Functions

The program contains the following main functions:

generate_key_matrix()
prepare_plaintext()
create_digraphs()
playfair_encrypt()
playfair_decrypt()
digraph_frequency()
verify()

Project Structure
Playfair-Cipher/
│
├── playfair.cpp
└── README.md

License

This project is intended for educational purposes.
