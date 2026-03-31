from PIL import Image
import sympy

img = Image.open("output.png")
pixels = list(img.getdata())  # flat list of (R, G, B) tuples

bits = []
total_pixels = len(pixels)  # 1024*1024 = 1,048,576

# Generate primes up to total pixel count
primes = list(sympy.primerange(0, total_pixels))

for p in primes:
    r, g, b = pixels[p]
    bits.append(r & 1)
    bits.append(g & 1)
    bits.append(b & 1)

# Convert bits to bytes
result = bytearray()
for i in range(0, len(bits) - 7, 8):
    byte = 0
    for j in range(8):
        byte = (byte << 1) | bits[i + j]
    result.append(byte)

# Find and print flag
text = result.decode('latin-1')
flag_start = text.find('hackzero{')
if flag_start != -1:
    flag_end = text.find('}', flag_start) + 1
    print(text[flag_start:flag_end])
else:
    # Try printing readable ASCII
    readable = ''.join(c for c in text[:500] if 32 <= ord(c) <= 126)
    print(readable)
