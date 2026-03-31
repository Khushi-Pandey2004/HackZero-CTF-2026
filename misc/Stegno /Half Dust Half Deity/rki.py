digits = "00001100002020000203000021200002030000331000021000023200003310000120000110000010000001000000100000202000021000022000023100002210000203000021200002130000220000131000020300001330000100000020300001310000"

decoded = ""

for i in range(0, len(digits), 4):
    chunk = digits[i:i+4]
    if len(chunk) == 4:
        value = int(chunk, 4)
        if 32 <= value <= 126:   # printable ASCII
            decoded += chr(value)
        else:
            decoded += f"[{value}]"

print(decoded)
