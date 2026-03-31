from PIL import Image
import numpy as np

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i*i <= n:
        if n % i == 0 or n % (i+2) == 0: return False
        i += 6
    return True

img = Image.open("output.png").convert("RGB")
pixels = np.array(img)
r, g = pixels[:,:,0].astype(int), pixels[:,:,1].astype(int)

prime_cols = [c for c in range(1024) if is_prime(c)]

# Try R-G modulo variations at prime cols
for bit_val in [(0,1), (1,0)]:
    for msb in [True, False]:
        bits = []
        for y in range(1024):
            for x in prime_cols:
                rg = r[y,x] - g[y,x]
                if rg in [0, 1]:
                    bits.append(bit_val[rg])
        chars = []
        for i in range(0, len(bits)-7, 8):
            byte = sum(bits[i+j] << (7-j if msb else j) for j in range(8))
            chars.append(byte)
        result = bytes(chars)
        if b'hackzero' in result.lower():
            idx = result.lower().find(b'hackzero')
            print("FOUND!", result[idx:idx+60])
