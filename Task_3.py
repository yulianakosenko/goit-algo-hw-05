import timeit

# --- Boyer-Moore ---
def bad_character_table(pattern):
    bad_char = {}
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i
    return bad_char

def boyer_moore_search(text, pattern):
    bad_char = bad_character_table(pattern)
    matches = []
    m = len(pattern)
    n = len(text)
    shift = 0
    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
        if j < 0:
            matches.append(shift)
            shift += m - bad_char.get(text[shift + m], -1) if shift + m < n else 1
        else:
            skip = max(1, j - bad_char.get(text[shift + j], -1))
            shift += skip
    return matches

# --- Knuth-Morris-Pratt ---
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    lps = compute_lps(pattern)
    matches = []
    i = 0
    j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            matches.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches

# --- Rabin-Karp ---
def rabin_karp_search(text, pattern, prime=101):
    d = 256
    m = len(pattern)
    n = len(text)
    p = 0
    t = 0
    h = 1
    matches = []

    for i in range(m - 1):
        h = (h * d) % prime

    for i in range(m):
        p = (d * p + ord(pattern[i])) % prime
        t = (d * t + ord(text[i])) % prime

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                matches.append(i)
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t < 0:
                t += prime
    return matches

# --- Load text files ---
def load_text(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# --- Main benchmark ---
def benchmark_search_algorithms(text, pattern):
    bm_time = timeit.timeit(lambda: boyer_moore_search(text, pattern), number=10)
    kmp_time = timeit.timeit(lambda: kmp_search(text, pattern), number=10)
    rk_time = timeit.timeit(lambda: rabin_karp_search(text, pattern), number=10)

    print(f"Pattern: '{pattern}'")
    print(f"Boyer-Moore: {bm_time:.6f} seconds")
    print(f"KMP:         {kmp_time:.6f} seconds")
    print(f"Rabin-Karp:  {rk_time:.6f} seconds")
    print()

    return {"BM": bm_time, "KMP": kmp_time, "RK": rk_time}

# --- Run ---
if __name__ == "__main__":
    text1 = load_text('article1.txt')
    text2 = load_text('article2.txt')

    # Choose patterns
    pattern_real_1 = text1[100:120]  # реальний підрядок з text1
    pattern_fake_1 = "qwertyuiopasdfgh"  # вигаданий підрядок

    pattern_real_2 = text2[200:220]  # реальний підрядок з text2
    pattern_fake_2 = "zxcvbnmlkjhgfdsa"  # вигаданий підрядок

    print("=== Article 1 ===")
    times1_real = benchmark_search_algorithms(text1, pattern_real_1)
    times1_fake = benchmark_search_algorithms(text1, pattern_fake_1)

    print("=== Article 2 ===")
    times2_real = benchmark_search_algorithms(text2, pattern_real_2)
    times2_fake = benchmark_search_algorithms(text2, pattern_fake_2)

    # Summary
    def best_algo(times):
        return min(times, key=times.get)

    print("=== Summary ===")
    print(f"Article 1 (real pattern): {best_algo(times1_real)}")
    print(f"Article 1 (fake pattern): {best_algo(times1_fake)}")
    print(f"Article 2 (real pattern): {best_algo(times2_real)}")
    print(f"Article 2 (fake pattern): {best_algo(times2_fake)}")
