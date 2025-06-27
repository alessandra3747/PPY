
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ZADANIE 1 
x = np.linspace(-5, 5, 100)

y1 = 2 * x + 1
y2 = x**2 - 3 * x + 2

plt.figure(figsize=(8, 5))
plt.plot(x, y2, label='y = x^2 - 3x + 2', color='blue')
plt.scatter(x, y1, label='y = 2x + 1', color='red')

plt.title('Wykres funkcji matematycznych')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

# ZADANIE 2 
uczniowie = ['Anna', 'Bartek', 'Cezary', 'Daria', 'Ela']
matematyka = [78, 88, 95, 72, 80]
fizyka = [85, 79, 92, 68, 82]
chemia = [92, 85, 88, 74, 78]

fig, axs = plt.subplots(1, 3, figsize=(15, 5))

axs[0].bar(uczniowie, matematyka, color='green')
axs[0].set_title('Wyniki z matematyki')
axs[0].set_xlabel('Uczniowie')
axs[0].set_ylabel('Wynik')

axs[1].bar(uczniowie, fizyka, color='blue')
axs[1].set_title('Wyniki z fizyki')
axs[1].set_xlabel('Uczniowie')
axs[1].set_ylabel('Wynik')

axs[2].bar(uczniowie, chemia, color='orange')
axs[2].set_title('Wyniki z chemii')
axs[2].set_xlabel('Uczniowie')
axs[2].set_ylabel('Wynik')

plt.tight_layout()
plt.show()

# ZADANIE 3
df = pd.read_excel('Dane_Pandas.xlsx')

df.set_index('Imie', inplace=True)

dni_tygodnia = df.columns.tolist()

plt.figure(figsize=(10, 6))
kolory = ['blue', 'green', 'orange']
style = ['-', '--', '-.']

for idx, user in enumerate(df.index):
    kroki = df.loc[user]
    max_dzien = kroki.idxmax()
    max_kroki = kroki.max()
    
    plt.plot(dni_tygodnia, kroki, label=user, color=kolory[idx], linestyle=style[idx])
    plt.plot(max_dzien, max_kroki, marker='*', color=kolory[idx], markersize=12)


plt.title('Liczba krokow uzytkownikow w ciagu tygodnia')
plt.xlabel('Dzien tygodnia')
plt.ylabel('Liczba krokow')
plt.legend(title='Uzytkownik')
plt.grid(True)
plt.tight_layout()
plt.show()
