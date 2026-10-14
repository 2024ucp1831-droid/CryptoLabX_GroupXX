from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16

def pad(data):
    n = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([n] * n)

def create_challenge(message):
    key = get_random_bytes(16)
    iv = get_random_bytes(BLOCK_SIZE)
    ciphertext = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(message))

    def oracle(test_iv, test_ciphertext):
        try:
            decrypted = AES.new(key, AES.MODE_CBC, test_iv).decrypt(test_ciphertext)
            n = decrypted[-1]
            return 1 <= n <= BLOCK_SIZE and decrypted[-n:] == bytes([n] * n)
        except (ValueError, IndexError):
            return False

    return iv, ciphertext, oracle

def padding_oracle_attack(iv, ciphertext, oracle):
    queries = 0
    result = b""
    blocks = [ciphertext[i:i + BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]

    for i, block in enumerate(blocks):
        previous = iv if i == 0 else blocks[i - 1]
        intermediate = [0] * BLOCK_SIZE

        for padding in range(1, BLOCK_SIZE + 1):
            index = BLOCK_SIZE - padding
            crafted = bytearray(BLOCK_SIZE)

            for j in range(index + 1, BLOCK_SIZE):
                crafted[j] = intermediate[j] ^ padding

            found = False

            for guess in range(256):
                crafted[index] = guess ^ padding
                queries += 1

                if not oracle(bytes(crafted), block):
                    continue

                if padding < BLOCK_SIZE:
                    check = bytearray(crafted)
                    check[index - 1] ^= 1
                    queries += 1

                    if not oracle(bytes(check), block):
                        continue

                intermediate[index] = guess
                found = True
                break

            if not found:
                raise RuntimeError("Plaintext recovery failed")

        result += bytes(a ^ b for a, b in zip(intermediate, previous))

    n = result[-1]

    if n < 1 or n > BLOCK_SIZE or result[-n:] != bytes([n] * n):
        raise ValueError("Recovered plaintext has invalid padding")

    return result[:-n], queries

iv, ciphertext, oracle = create_challenge(b"Padding oracle attack demonstration")
plaintext, queries = padding_oracle_attack(iv, ciphertext, oracle)

print("Ciphertext:", ciphertext.hex())
print("Recovered plaintext:", plaintext.decode())
print("Oracle queries:", queries)
