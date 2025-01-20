from galois_field import Galois_Field


def affine_decrypt(gf: Galois_Field, ciphertext, alpha, beta):
    # Расшифрование текста с использованием аффинного шифра.
    alpha_inv = gf.find_inv(alpha) # Поиск обратного элемента
    plaintext = [] # Открытый текст
    for y in ciphertext:
        x = gf.multiply(alpha_inv, gf.add(y, [-b for b in beta]))
        plaintext.append(x)
    return plaintext
