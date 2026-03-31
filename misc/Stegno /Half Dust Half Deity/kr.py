from collections import Counter

text = open("poetry.txt", encoding="utf-8").read()
hidden = [c for c in text if ord(c) > 127]

print(Counter(hidden))
