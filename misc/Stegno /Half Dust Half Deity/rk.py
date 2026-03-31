text = open("poetry.txt", encoding="utf-8").read()

mapping = {
    '\u200b': '0',
    '\u202a': '1',
    '\u2063': '2',
    '\u200d': '3'
}

digits = ""

for c in text:
    if c in mapping:
        digits += mapping[c]

print(digits[:200])
