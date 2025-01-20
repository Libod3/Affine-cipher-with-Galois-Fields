from galois_field import Galois_Field


def text_to_field(alphabet, text, gf: Galois_Field):
    # Преобразует строку в элементы поля Галуа на основе заданного алфавита
    index_map = {char: idx for idx, char in enumerate(alphabet)} # Словарь вида: {Символ : Порядковый номер}
    result = []
    for char in text:
        index = index_map[char]
        element = gf.elements[index]
        result.append(element)
    return result


def field_to_text(alphabet, field_elements, gf: Galois_Field):
    # Преобразует элементы поля Галуа обратно в строку
    # Словарь вида: {Тапл с коэф-ми : Порядковый номер}
    reverse_map = {tuple(value): idx for idx, value in enumerate(gf.elements)}
    result = []
    for element in field_elements:
        index = reverse_map[tuple(element)]
        result.append(alphabet[index])
    return ''.join(result) # Сделано так, чтобы выводилась именно строка, а не list по charам
