#S30395

#ZADANIE 1
def zadanie1a():
    number = (int)(input("1a. Podaj liczbę: "))
    for i in range(number, number+10):
        print(i)

zadanie1a()

def zadanie1b():
    number = (int)(input("1b. Podaj liczbę: "))

    while number > 20:
        number = (int)(input("1b. Podaj liczbę mniejszą od 20: "))

    wiersze = [x for x in range(1, number+1)]
    kolumny = [x for x in range(1, number+1)]

    for i in wiersze:
        for j in kolumny:
            print(i*j, end="\t")
        print()

zadanie1b()

def zadanie1c():
    number = (int)(input("1c. Podaj liczbę: "))
    for i in range(number):
        number += i
    print(number)

zadanie1c()

#ZADANIE 2
def zadanie2():
    number = (int)(input("2. Podaj liczbę: "))

    print("\nWariant A")
    for i in range(number, 0 ,-1):
        for j in range(i, 0 ,-1):
            if j % 5 == 0:
               print("#", end=" ")
            elif j % 2 == 0:
               print(j * (-1), end=" ")
            else:
                print(j, end=" ")
        print()

    print("\nWariant B")
    for i in range(number, 0, -1):
        for j in range(i, 0, -1):
            print(j, end=" ")
        print()

zadanie2()

def zadanie3a():
    n = 1123712836
    print(len(str(n)))

zadanie3a()

def zadanie3b():
    n = int(1123712836)
    length = 0

    while n > 0:
        length += 1
        n = round(n/10, 0)

    print(length)

zadanie3b()


#ZADANIE 4
def zadanie4():
    a = (int)(input("Podaj poczatek zakresu: "))
    b = (int)(input("Podaj koniec zakresu: "))

    for i in range(a,b):
        if czyPierwsza(i):
            print(i)


def czyPierwsza(number):
    if number <= 1:
        return False

    for i in range(2, number):
        if number % i == 0:
            return False

    return True

zadanie4()
