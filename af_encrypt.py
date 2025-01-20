from galois_field import Galois_Field


def affine_encrypt(gf: Galois_Field, plaintext, alpha, beta):
    # Шифрование текста с использованием аффинного шифра.
    ciphertext = [] # Шифртекст
    for x in plaintext:
        y = gf.add(gf.multiply(alpha, x), beta)
        ciphertext.append(tuple(y))
    return ciphertext
