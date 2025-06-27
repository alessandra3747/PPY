import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame


def zadanie1():

    lista_liczb : list[int] = []

    for i in range(10_000):
        lista_liczb.append(np.random.randint(-3, 21))

    srednia : float = np.average(lista_liczb)
    mediana : float = np.median(lista_liczb)
    maksymalna_wartosc : int = np.max(lista_liczb)
    minimalna_wartosc : int = np.min(lista_liczb)
    odchylenie_standardowe : float = np.std(lista_liczb)
    odchylenie_od_sredniej : float = srednia - 3 * odchylenie_standardowe

    counter : int = 0
    for liczba in lista_liczb:
        if liczba < odchylenie_od_sredniej:
            counter += 1

    procent_liczb : int = counter / len(lista_liczb) * 100

    print(f"Średnia: {srednia}\n"
          f"Mediana: {mediana}\n"
          f"Maksymalna wartość: {maksymalna_wartosc}\n"
          f"Minimalna wartość: {minimalna_wartosc}\n"
          f"Procent liczb mniejszych: {procent_liczb}%"
          f"\n=======================================\n")



    df_liczby : DataFrame = pd.DataFrame({'liczba' : list(set(lista_liczb))})
    df_liczby['wystepowanie'] = df_liczby['liczba'].map(lista_liczb.count)
    df_liczby['czy_ujemna'] = df_liczby['liczba'] < 0

    df_liczby = df_liczby[df_liczby['liczba'] >= 0]

    print(df_liczby[:])


    plt.figure(figsize=(10, 6))
    plt.bar(df_liczby['liczba'], df_liczby['wystepowanie'])
    plt.xlabel('Liczba')
    plt.ylabel('Czestość występowania')

    plt.show()

    nazwa_pliku : str = str(f"Dane_{srednia}_{odchylenie_standardowe}.csv")
    df_liczby.to_csv(nazwa_pliku)


zadanie1()


#def fang(nums : list, target : int):
#    sorted(nums)
#    for i in range(len(nums)):
#        if nums[i] + nums[len(nums) - 1 - i] == target:
#            return [i, len(nums) - 1 - i]
#
#print(fang([2,7,11,15], 9))