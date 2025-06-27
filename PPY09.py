import math

class Wielokat:

    def __init__(self):
        self.n : int = 0
        self.boki = []

    def askNSides(self):
        self.n = int(input("Podaj ilość boków wielokąta: "))

    def inputSides(self):
        self.boki = []
        for i in range(self.n):
            bok = float(input(f"Podaj długość boku {i+1}: "))
            self.boki.append(bok)

    def dispSides(self):
        for i, bok in enumerate(self.boki, 1):
            print(f"Bok {i}: {bok} cm")

    def whatShape(self):
        if not self.boki or self.n == 0:
            print("Boki się nie zgadzają...")
            return
        if self.n == 3:
            a, b, c = sorted(self.boki)
            if a + b > c:
                print("Ten wielokąt jest trójkątem.")
            else:
                print("Ten wielokąt nie jest trójkątem.")
        elif self.n == 4:
            if all(bok == self.boki[0] for bok in self.boki):
                print("Ten wielokąt jest kwadratem.")
            else:
                print("Ten wielokąt nie jest kwadratem.")
        else:
            print("Ten wielokąt nie jest trójkątem ani kwadratem.")

    def circuit(self) -> float:
        if not self.boki:
            print("Boki nie mogą być puste...")
            return 0
        obwod : float = sum(self.boki)
        print(f"Obwód wynosi: {obwod} cm")
        return obwod



class Trojkat(Wielokat):

    def __init__(self):
        super().__init__()
        self.n = 3

    def area(self) -> float:
        if not self.boki:
            print("Boki nie mogą być puste...")
            return 0
        a, b, c = self.boki
        s : float = (a + b + c) / 2
        pole : float = math.sqrt(s * (s - a) * (s - b) * (s - c))
        print(f"Pole trójkąta: {pole:.2f} cm^2")
        return pole

    def isright(self) -> bool:
        if not self.boki:
            print("Boki nie mogą być puste...")
            return False
        a, b, c = sorted(self.boki)
        if abs(c**2 - (a**2 + b**2)) < 1e-5:
            print("To jest trójkąt prostokątny.")
            return True
        else:
            print("To nie jest trójkąt prostokątny.")
            return False



class Kwadrat(Wielokat):

    def __init__(self):
        super().__init__()
        self.n = 1

    def inputSides(self):
        bok = float(input("Podaj długość boku kwadratu: "))
        self.boki = [bok]

    def area(self) -> float:
        if not self.boki:
            print("Boki nie mogą być puste...")
            return 0
        bok = self.boki[0]
        pole : float = bok * bok
        print(f"Pole kwadratu: {pole:.2f} cm^2")
        return pole

    def circuit(self) -> float:
        if not self.boki:
            print("Boki nie mogą być puste...")
            return 0
        bok = self.boki[0]
        obwod : float = 4 * bok
        print(f"Obwód kwadratu: {obwod} cm")
        return obwod
