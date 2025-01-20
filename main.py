from galois_field import Galois_Field
from af_encrypt import affine_encrypt
from af_decrypt import affine_decrypt
import text_converter


if __name__ == '__main__':
    alp = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

    text = input("Введите текст: ")
    mode = int(input("Введите, что хотети сделать:\n 1 - Зашифровать \n 2 - Расшифровать \n "))
    alpha = str(input("Введите альфу вида: 00000: "))
    alpha = [int(i) for i in alpha]
    beta = str(input("Введите бету вида: 00000: "))
    beta = [int(i) for i in beta]
    poly = input("Введите коэффициенты возможной функции над полем вида 0,0,0,0,0"
                 ", нажмите Enter если не хотите задавать функцию")
    if poly == "":
        poly = None
    else:
        poly = [int(i) for i in poly.split(",")]

    gf = Galois_Field(2, 5, poly)
    plaintext = text_converter.text_to_field(alp, text, gf)
    if mode == 1:
        ciphertext = affine_encrypt(gf, plaintext, alpha, beta)
    elif mode == 2:
        ciphertext = affine_decrypt(gf, plaintext, alpha, beta)
    else:
        print("Error 01: выбран не тот mode")

    decrypted_text = text_converter.field_to_text(alp, ciphertext, gf)

    print(f"Результат программы: {decrypted_text}")

