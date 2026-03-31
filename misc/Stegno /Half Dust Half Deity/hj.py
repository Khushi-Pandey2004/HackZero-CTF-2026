from itertools import permutations

text = open("poetry.txt", encoding="utf-8").read()

symbols = ['\u200b', '\u202a', '\u2063', '\u200d']

# extract only relevant chars
filtered = [c for c in text if c in symbols]

for perm in permutations('0123'):
    mapping = dict(zip(symbols, perm))
    
    digits = "".join(mapping[c] for c in filtered)
    
    decoded = ""
    for i in range(0, len(digits), 4):
        chunk = digits[i:i+4]
        if len(chunk) == 4:
            decoded += chr(int(chunk, 4))
    
    if "hackzero" in decoded.lower():
        print("FOUND:", mapping)
        print(decoded)
        break
