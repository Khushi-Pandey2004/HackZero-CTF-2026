#!/usr/bin/env python3
import sys

SYMBOLS = {
    '\u200b': 0,  # ZERO WIDTH SPACE
    '\u200d': 1,  # ZERO WIDTH JOINER
    '\u202a': 2,  # LEFT-TO-RIGHT EMBEDDING
    '\u2063': 3,  # INVISIBLE SEPARATOR
    '\u202d': 4,  # LEFT-TO-RIGHT OVERRIDE
}

NAMES = {
    '\u200b': 'U+200B',
    '\u200d': 'U+200D',
    '\u202a': 'U+202A',
    '\u2063': 'U+2063',
    '\u202d': 'U+202D',
}

def extract_zw(text):
    return [c for c in text if c in SYMBOLS]

def decode_blocks(chars):
    if len(chars) % 7 != 0:
        print(f"[!] Warning: zero-width char count {len(chars)} is not divisible by 7")

    blocks = [chars[i:i+7] for i in range(0, len(chars), 7)]
    out = []

    for idx, block in enumerate(blocks, 1):
        if len(block) < 7:
            continue

        prefix = block[:4]
        payload = block[4:]

        if prefix != ['\u200b'] * 4:
            print(f"[!] Block {idx} has unexpected prefix: {' '.join(NAMES.get(c, hex(ord(c))) for c in prefix)}")

        a, b, c = [SYMBOLS[x] for x in payload]
        value = a * 25 + b * 5 + c
        out.append(chr(value))

    return ''.join(out)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} poetry.txt")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    zw = extract_zw(text)
    print(f"[+] Extracted {len(zw)} zero-width characters")

    decoded = decode_blocks(zw)
    print("[+] Decoded message:")
    print(decoded)

if __name__ == "__main__":
    main()
