from math import isqrt
import hashlib, subprocess

p = 8736489073805684086305179507451312145336960198850222450321684285045258466628525808781552246900007804506276394992600728538533608361706639189532331964901531
g = 2
A = 2794996066442934640383396708993220584783762169186726070188366297468316333265452428474082701535690342706174889597372484008702943319781202470240884210613693
B = 1210454350578824211787039637709213524440747952483190753841197066710749405257527570548081311766060600166395746681022324544415844366753788799012419699450666

def try_decrypt(shared):
    shared_bytes = shared.to_bytes((shared.bit_length()+7)//8, 'big')
    shared_hex = hex(shared)[2:]
    passphrases = [
        str(shared),
        shared_hex,
        hashlib.sha256(shared_bytes).hexdigest(),
        hashlib.sha256(str(shared).encode()).hexdigest(),
        hashlib.sha256(shared_hex.encode()).hexdigest(),
        hashlib.sha512(shared_bytes).hexdigest(),
        hashlib.md5(shared_bytes).hexdigest(),
    ]
    for pp in passphrases:
        r = subprocess.run(
            ['gpg','--batch','--yes','--passphrase', pp, '--decrypt', 'flag.txt.gpg'],
            capture_output=True, text=True
        )
        if r.returncode == 0:
            print(f"[+] FLAG with passphrase '{pp[:40]}': {r.stdout.strip()}")
            return True
    return False

# ===== APPROACH: Full BSGS up to 2^50 =====
# p is 511 bits but maybe private key is intentionally small (CTF trick)

def bsgs(g, h, p, limit):
    """BSGS to find x where g^x = h mod p, x < limit"""
    m = isqrt(limit) + 1
    print(f"[*] BSGS: m={m}, building table of {m} entries...")
    
    # Baby steps: table[g^j mod p] = j
    table = {}
    gj = 1
    for j in range(m):
        table[gj] = j
        gj = gj * g % p
    
    print(f"[*] Table built. Running giant steps...")
    # Giant steps: h * (g^-m)^i for i in range(m)
    gm_inv = pow(pow(g, m, p), p-2, p)
    gamma = h
    for i in range(m + 1):
        if gamma in table:
            x = i * m + table[gamma]
            if x < limit:
                return x
        gamma = gamma * gm_inv % p
        if i % 500000 == 0:
            print(f"  giant step {i}/{m}...")
    return None

# Try limits: 2^40, 2^48, 2^56 (increasing)
for bits in [40, 44, 48]:
    limit = 2**bits
    print(f"\n[*] Trying BSGS with limit 2^{bits} = {limit}")
    b = bsgs(g, B, p, limit)
    if b is not None:
        print(f"[+] Found b = {b}")
        shared = pow(A, b, p)
        print(f"[+] Shared secret = {shared}")
        if try_decrypt(shared):
            break
        else:
            print("[-] Wrong passphrase format, but secret found!")
            # Also try with a (solve for A's private key)
            a = bsgs(g, A, p, limit)
            if a:
                shared2 = pow(B, a, p)
                print(f"[+] Shared via a={a}: {shared2}")
                try_decrypt(shared2)
    else:
        print(f"[-] Not found within 2^{bits}")
