from itertools import permutations

text = open("poetry.txt", encoding="utf-8").read()

symbols = ['\u200b', '\u202a', '\u2063', '\u200d', '\u202d']

filtered = [c for c in text if c in symbols]

for perm in permutations('01234'):
    mapping = dict(zip(symbols, perm))
    
    digits = "".join(mapping[c] for c in filtered)
    
    decoded = ""
    
    # try grouping sizes
    for size in [3, 4, 5]:
        temp = ""
        for i in range(0, len(digits), size):
            chunk = digits[i:i+size]
            if len(chunk) == size:
                try:
                    temp += chr(int(chunk, 5))
                except:
                    pass
        
        if "hackzero" in temp.lower():
            print("FOUND:", mapping, "size:", size)
            print(temp)
            exit()
