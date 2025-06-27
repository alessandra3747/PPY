#s30395
class FunkcjaKwadratowa:

    def __init__(self, a : float = None, b : float = None, c: float = None):
        self.a = float(input("Podaj wartość a: ")) if a is None else a
        self.b = float(input("Podaj wartość b: ")) if b is None else b
        self.c = (input("Podaj wartość c: ")) if c is None else c


    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("a musi być typu int lub float")
        if value == 0:
            raise ValueError("a nie może być zerem")
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("b musi być typu int lub float")
        self._b = value

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("c musi być typu int lub float")
        self._c = value


    def my_decorator(func):
        def opakowanie(*args, **kwargs):
            miejsca = func(*args, **kwargs)
            if miejsca == None:
                print("Brak miejsc zerowych.")
            elif len(miejsca) == 1:
                print("Funkcja ma jedno miejsce zerowe")
            else :
                print("Funkcja ma dwa miejsca zerowe")
            return miejsca
        return opakowanie


    @my_decorator
    def rozwiaz(self):
        delta : float = self.b**2 - (4 * self.a * self.c)
        if delta > 0:
            x1 = (-self.b - delta**(1/2)) / 2 * self.a
            x2 = (-self.b + delta**(1/2)) / 2 * self.a
            return x1,x2
        elif delta == 0:
            return -self.b / 2 * self.a
        else:
            return None


    def __add__(self, other):
        if not isinstance(other, FunkcjaKwadratowa):
            raise TypeError("Można dodawać tylko obiekty klasy FunkcjaKwadratowa")
        return FunkcjaKwadratowa(self.a + other.a, self.b + other.b, self.c + other.c)

    def __sub__(self, other):
        if not isinstance(other, FunkcjaKwadratowa):
            raise TypeError("Można odejmować tylko obiekty klasy FunkcjaKwadratowa")
        return FunkcjaKwadratowa(self.a - other.a, self.b - other.b, self.c - other.c)


    def nalezy(self, punkt) -> bool:
        x, y = punkt
        return y == self.a * x ** 2 + self.b * x + self.c



test1 = FunkcjaKwadratowa(1,-4,-5)
test1.rozwiaz()
print(test1.nalezy((2,-9)))

test2 = FunkcjaKwadratowa(1,1,1)
test3 = test1 + test2
test3.rozwiaz()