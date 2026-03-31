from PIL import Image

def sieve(n):
    is_prime = bytearray([1]) * (n + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = bytearray(len(is_prime[i*i::i]))
    return is_prime

img = Image.open("output.png")
pixels = list(img.getdata())
N = len(pixels)
is_prime = sieve(N)

# Try each channel independently AND combined
for mode in ['R', 'G', 'B', 'RGB']:
    bits = []
    for i, px in enumerate(pixels):
        if is_prime[i]:
            if mode == 'RGB':
                bits += [px[0]&1, px[1]&1, px[2]&1]
            elif mode == 'R': bits.append(px[0]&1)
            elif mode == 'G': bits.append(px[1]&1)
            elif mode == 'B': bits.append(px[2]&1)
    
    result = bytearray()
    for i in range(0, len(bits)-7, 8):
        result.append(int(''.join(map(str, bits[i:i+8])), 2))
    
    text = result.decode('latin-1', errors='replace')
    idx = text.find('hackzero{')
    if idx != -1:
        print(f"[{mode}] FLAG: {text[idx:text.find('}',idx)+1]}")
    else:
        print(f"[{mode}] No flag. Sample: {text[:60]}")
