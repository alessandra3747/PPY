import os
import shutil
import string
from datetime import datetime


#ZADANIE 1
def zadanie_1():

    try:
        os.makedirs("zajecia")
    except FileExistsError:
        pass


    with open("dzis.txt", "w") as file:
        date = datetime.now()
        file.write(date.strftime("%d.%m.%Y %H:%M:%S"))



    shutil.move("dzis.txt", "zajecia/dzis.txt")



    lista: list[int] = [i for i in range(1, 15)]


    with open("zajecia/liczby.txt", "a") as file:
        for liczba in lista:
            file.write(f"{liczba}\n")


    with open("zajecia/liczby_parzyste.txt", "w") as file:
        for liczba in lista:
            if liczba % 2 == 0:
                file.write(f"{liczba}\n")

    with open("zajecia/liczby_nieparzyste.txt", "w") as file:
        for liczba in lista:
            if liczba % 2 != 0:
                file.write(f"{liczba}\n")


    katalogi : list[str] = [file for file in os.listdir("zajecia")]

    print(katalogi)


zadanie_1()


#ZADANIE 2
def policz_wystąpienia(sciezka_pliku : str) -> dict:

    try:
        with open(sciezka_pliku, "r", encoding="utf-8") as file:
            tekst = file.read()
    except FileNotFoundError:
        return {}

    tekst.translate(str.maketrans('', '', string.punctuation)).lower()

    slowa = tekst.split()

    wystapienia : dict = {}

    for slowo in slowa:
        wystapienia[slowo] = wystapienia.get(slowo, 0) + 1

    return wystapienia


wystapienia = policz_wystąpienia("wiki.txt")

for (slowo, liczba) in wystapienia.items():
    print(f"{slowo} : {liczba}")



#ZADANIE FANG
def zadanie_fang(ceny: list[int]) -> int:

    min_cena = ceny[0]
    maks_zysk = 0

    for i in ceny:
        min_cena = min(i, min_cena)
        maks_zysk = max(maks_zysk, i - min_cena)

    return maks_zysk


print(zadanie_fang([7, 1, 5, 3, 6, 4]))




