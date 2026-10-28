from collections import Counter

def analyze_file(filename):
    with open(filename, "r") as file:
        data = file.read()

    print("Characters:", len(data))
    print("Words:", len(data.split()))
    print("Lines:", len(data.splitlines()))
    print("Unique Characters:", len(set(data)))

    print("\nLetter Frequency:")
    for c, n in Counter(data.lower()).items():
        if c.isalpha():
            print(c, ":", n)
