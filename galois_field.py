from itertools import product


class Galois_Field:
    def __init__(self, p, n, polynomial=None):
        self.p = p
        self.n = n
        self.size = p ** n

        # Тут проверяем, передали ли мы многочлен
        if polynomial is None:
            self.polynomial = list(self.create_polynomial())
        else:
            # Сделано так, чтобы формат задачи был в виде листа,
            # Состоящего из int - значений коэффициентов, а их позиция показывала степень x
            self.polynomial = [coeff % p for coeff in polynomial]
            # Пример: [1, 0, 1, 1] -> (1 * x^3) + (0 * x^2) + (1 * x^1) + (1 * x^0) = x^3 + x + 1

        self.elements = self._build_field()

    def _build_field(self):
        # Тут создаём элементы поля Галуа
        elements = []
        for coeffs in product(range(self.p), repeat=self.n):
            elements.append(list(coeffs))
        return elements

    def is_polynomial_irreducible(self, poly):
        # Функция поиска неприводимого многочлена
        def simple_multiply(a, b): # Тут нужна своя функция умножения, иначе ломается
            result_degree = len(a) + len(b) - 2
            result = [0] * (result_degree + 1)

            for i, coeff_a in enumerate(a):
                for j, coeff_b in enumerate(b):
                    result[i + j] += coeff_a * coeff_b
                    result[i + j] %= self.p

            return result

        gf_temp = Galois_Field(self.p, self.n - 1, poly[:]) # Создаём временное поле, чтобы брать оттуда элементы
        for element in gf_temp.elements[1:]:  # Пропускаем 0
            result = [1]
            for _ in range(self.size - 1):
                result = simple_multiply(result, element)
                if result == [0] * self.n:
                    return False
        return True

    def create_polynomial(self) -> tuple or str:
        # Тут создаём всевозможные многочлены (tuple тк 1-Защита от глупости; 2-Product создаёт tuplы))
        # range(p) -> 0, 1, ... p-1,
        # repeat=(n + 1) показывает длину многочлена n + 1 (k*x^n + l*x^n-1 + ... + z*x^0)
        for coeffs in product(range(self.p), repeat=(self.n + 1)):
            # Проверка, что многочлен именно степени n, не меньше
            if coeffs[-1] == 0:
                continue
            elif self.is_polynomial_irreducible(coeffs):
                return coeffs
            else:
                return "Таких многочленов не найдено"

    def add(self, a, b):
        # Чтобы сложить два многочлена–элемента поля Галуа F_{p^n}, необходимо сложить их коэффициенты при
        # соответствующих степенях и привести полученные значения по модулю p.
        return [(x + y) % self.p for x, y in zip(a, b)]
        # zip() - встроенное чудо в python,
        # проходит по элементам и останавливается когда в одном из объектов заканчиваются объекты

    def multiply(self, a, b):
        result_degree = len(a) + len(b) - 2 # Тк степень_a = a-1, cтепень_b = b-1
        result = [0] * (result_degree + 1)

        # Для начала перемножим коэффициенты многочленов
        for i, coeff_a in enumerate(a):
            for j, coeff_b in enumerate(b):
                result[i + j] += coeff_a * coeff_b
                result[i + j] %= self.p

        # Далее нужно будет выполнять деление полученного многочлена, степень которого может быть выше n-1,
        # на неприводимый многочлен f принадл. F_p[X]
        while len(result) > self.n:
            # Тут пойдём по принципу: берём старший член, делим на него -> берем след. старший член
            leading_coeff = result[-1]
            for i in range(len(self.polynomial)): # подсказка: a + b = len -> -b = -len + a
                result[-(len(self.polynomial) - i)] -= leading_coeff * self.polynomial[i]
                result[-(len(self.polynomial) - i)] %= self.p
            result.pop() # Удаляем старший коэффициент

        return result

    def find_gen(self):
        # Функция поиска образующего элемента
        for element in self.elements[1:]:  # Пропускаем 0
            powers = set() # Используем тип данных set чтобы не добавлять повторений
            current = element # Хранит текущий элемент (вспомогательная переменная)
            for _ in range(self.size - 1): # _ тк нам все равно какое значение
                powers.add(tuple(current)) # переводим в тапл чтобы работало умножение
                current = self.multiply(current, element)
            if len(powers) == self.size - 1:
                return element
        return None

    def find_inv(self, a):
        # Функция поиска обратного элемента
        for element in self.elements:
            # Суть в том, что a * b = 1 когда a и b - обратные элементы, а 1 - мультипликативная единица
            # Но в полях мультипликативная единица представлена как [1] + [0] * (self.n - 1) (1 + 0x + 0x^2 ...)
            if self.multiply(a, element) == [1] + [0] * (self.n - 1):
                return element
        return None
