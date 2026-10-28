import sys, math
from collections import Counter

def analyze(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    length = len(data)
    if length == 0:
        return None
    
    counts = Counter(data)
    entropy = -sum((c/length) * math.log2(c/length) for c in counts.values())
    
    expected = length / 256.0
    chi_sq = sum(((counts[i] - expected) ** 2) / expected for i in range(256))
    
    ones = sum(bin(b).count('1') for b in data)
    bit_1_ratio = ones / (length * 8)
    
    sum_x = sum(data)
    sum_x2 = sum(b * b for b in data)
    dot_prod = sum(data[i] * data[(i + 1) % length] for i in range(length))
    var_denom = sum_x2 - (sum_x ** 2) / length
    serial_corr = (dot_prod - (sum_x ** 2) / length) / var_denom if var_denom != 0 else 0
    
    return {
        "file": filename,
        "entropy": entropy,
        "chi_sq": chi_sq,
        "bit_1_ratio": bit_1_ratio,
        "serial_corr": serial_corr
    }

if __name__ == "__main__":
    # Includes all 3 Linux output files and windows_random.bin by default
    default_files = ["urandom_1mb.bin", "openssl_1mb.bin", "dotnet_1mb.bin", "windows_random.bin"]
    files = sys.argv[1:] if len(sys.argv) > 1 else default_files
    results = []

    for fname in files:
        try:
            res = analyze(fname)
            if res:
                results.append(res)
        except FileNotFoundError:
            print(f"Warning: File '{fname}' not found in current directory.")

    if results:
        print("\n=== INDIVIDUAL RESULTS ===")
        for r in results:
            print(f"\nFile: {r['file']}")
            print(f"Entropy:            {r['entropy']:.6f} bits/byte (Ideal: 8.000000)")
            print(f"Chi-Square:         {r['chi_sq']:.2f} (Ideal: ~255.0)")
            print(f"Bit Ratio (1s):     {r['bit_1_ratio']:.4%} (Ideal: 50.0%)")
            print(f"Serial Correlation: {r['serial_corr']:.6f} (Ideal: 0.000000)")

        print("\n=== COMPARISON TABLE ===")
        print(f"| {'File':<20} | {'Entropy (bits/byte)':<20} | {'Chi-Square':<12} | {'Bit Ratio (1s)':<15} | {'Serial Correlation':<18} |")
        print("|" + "-"*22 + "|" + "-"*22 + "|" + "-"*14 + "|" + "-"*17 + "|" + "-"*20 + "|")
        for r in results:
            print(f"| {r['file']:<20} | {r['entropy']:<20.6f} | {r['chi_sq']:<12.2f} | {r['bit_1_ratio']:<15.4%} | {r['serial_corr']:<18.6f} |")
