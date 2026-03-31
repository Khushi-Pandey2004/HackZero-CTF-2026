from PIL import Image
import re

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

bits = []
for i, (r, g, b) in enumerate(pixels):
    if is_prime[i]:
        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)

result = bytearray(
    int(''.join(map(str, bits[i:i+8])), 2)
    for i in range(0, len(bits) - 7, 8)
)

# Write to binary file — avoids ALL terminal encoding issues
with open("extracted.bin", "wb") as f:
    f.write(result)

print(f"Extracted {len(result)} bytes → extracted.bin")

# Search for flag
text = result.decode('latin-1', errors='replace')
matches = re.findall(r'hackzero\{[^}]*\}', text, re.IGNORECASE)
print(f"FLAG: {matches}" if matches else "Not found as plain text")
