import time

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

encrypttimestart = time.time()
def encrypt(message, n):
    # Rabin encryption: c = message^2 mod n
    return pow(message, 2, n)
encrypttimeend = time.time()

decrypttimestart = time.time()
def decrypt(ciphertext, p, q):
    # Rabin decryption: m = c^((p+1)/4) mod p, n = c^((q+1)/4) mod q
    mp = pow(ciphertext, (p + 1) // 4, p)
    mq = pow(ciphertext, (q + 1) // 4, q)

    # Use the Chinese Remainder Theorem to find the four possible square roots
    yp, yq = modinv(p, q), modinv(q, p)
    x1 = (yp * p * mq + yq * q * mp) % (p * q)
    x2 = n - x1
    x3 = (yp * p * mq - yq * q * mp) % (p * q)
    x4 = n - x3

    return x1, x2, x3, x4
decrypttimeend = time.time()

# Get input from the user
try:
    p = int(input("Enter a prime number (p): "))
    q = int(input("Enter another prime number (q): "))
    message = int(input("Enter the message to encrypt: "))

    n = p * q

    ciphertext = encrypt(message, n)
    print(f"Ciphertext: {ciphertext}")
    print("Encryption time: ", encrypttimeend - encrypttimestart)

    decrypted_values = decrypt(ciphertext, p, q)
    print("Decrypted values:", decrypted_values)
    print("Decryption time: ", decrypttimeend - decrypttimestart)
except ValueError:
    print("Invalid input. Please enter valid integers.")
