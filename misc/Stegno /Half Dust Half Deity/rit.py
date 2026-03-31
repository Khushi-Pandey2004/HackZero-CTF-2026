text = open("poetry.txt", "r", encoding="utf-8").read()

seq = [ord(c) for c in text if ord(c) in [0x200b, 0x202a, 0x2063, 0x200d, 0x202d]]
flat = [c for c in seq if c != 0x200b]

# Try all 24 permutations of the 4-char → 2-bit mapping
from itertools import permutations
chars = [0x200d, 0x202a, 0x2063, 0x202d]

for perm in permutations(range(4)):
    mapping = {chars[i]: format(perm[i], '02b') for i in range(4)}
    bits = ''.join(mapping[c] for c in flat)
    result = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    decoded = result.decode('utf-8', errors='replace')
    if 'hackzero' in decoded:
        print(decoded)
        break
