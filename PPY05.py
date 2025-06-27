from argparse import ArgumentError


#ZADANIE 1

class ZnakError(Exception):
    "Podnoszony, gdy znak w funkcji kalkulator jest niepoprawny"
    pass


def kalkulator(*args: int, **kwargs: str) -> float:


    if not all(isinstance(arg, int) for arg in args):
        raise ArgumentError("Args nie zawiera liczb!")

    if not all(isinstance(kwarg, str) for kwarg in kwargs):
        raise ArgumentError("Kwargs nie zawiera znaków!")

    if len(kwargs) >= len(args):
        raise ArgumentError("Ilość kwargs nie może być większa lub równa ilości args!")

    result: float = args[0]

    values = kwargs.values()

    for index, dzialanie in enumerate(values):
        match dzialanie:
          case '+':
            result += args[index+1]
          case '-':
            result -= args[index+1]
          case '*':
            result *= args[index+1]
          case '/':
            if args[index+1] == 0:
                raise ZeroDivisionError("Nie można dzielić przez zero!")
            result /= args[index+1]
          case _:
              raise ZnakError("Znak musi należeć do zbioru { +, -, *, / } !")

    return result


#print(kalkulator(1,3,2,działanie_1='+',działanie_2="-"))
#print(kalkulator(1,"3",2,działanie_1='+',działanie_2="-"))
#print(kalkulator(1,0,2,działanie_1='/',działanie_2="-"))
#print(kalkulator(1,3,działanie_1='+',działanie_2="-"))
#print(kalkulator(1,3,2,działanie_1='.',działanie_2="-"))


#ZADANIE 2

def wszystkie_podzbiory(zbior: list[int]) -> list[list[int]]:

    if not isinstance(zbior, list):
        raise ArgumentError("Argument nie jest listą!")

    for element in zbior:
        if not isinstance(element, int) and not isinstance(element, str) and not isinstance(element, float):
            raise ArgumentError("Argument nie jest int/float/str!")

    if len(zbior) == 0:
        raise ArgumentError("Lista jest pusta!")

    lista_zbiorow = [[]]

    for element in zbior:
        lista_zbiorow += [podzbior + [element] for podzbior in lista_zbiorow]

    return lista_zbiorow

#zbior = 1
#zbior = [ZnakError, 1]
#zbior = []
zbior = [1,2,3]

print(wszystkie_podzbiory(zbior))


#ZADANIE 3
def even_numbers(m: int):
    n = 0
    while n <= m:
        yield n
        n += 2

for number in even_numbers(10):
    print(number)


#ZADANIE FANG
def znajdz_najkrotsza_droge(siatka: list[list[int]]) -> int:
    kroki = 0
    for i in range(len(siatka)):
        if isdigit(siatka[i][i+1]):
            pass


