#ZADANIE 1
i = 2**(1/2)
i = i**2
print(i)
wzgledny_blad = abs((2-i))/2*100
print("Względny błąd wyniku wynosi: ")
print(wzgledny_blad)

#ZADANIE 2
print("Witaj, jak masz na imię?")
imie = input()
print("Miło Cię poznać " + imie)

#ZADANIE 3
print("Witaj!")
print("Wprowadź liczbę całkowitą")
liczba = int(input())
if liczba % 7 == 0 :
    print("Wprowadzona liczba jest podzielna przez 7 :)")
else :
    print("Wprowadzona liczba nie jest podzielna przez 7 :(")

#ZADANIE 4
print("Wprowadź trzy liczby")
print("Wprowadź pierwszą")
a = int(input())
print("Wprowadź drugą")
b = int(input())
print("Wprowadź trzecią")
c = int(input())

delta = a**2 - 4 * b * c

if delta < 0 :
    print("To równanie nie ma rozwiązań")
elif delta > 0 :
    print("To równanie ma dwa rozwiązania")
elif delta == 0 :
    print("To równanie ma jedno rozwiązanie")

#ZADANIE 5
print("Wprowadź wiek w latach")
wiek = int(input())

if wiek < 0 :
    print("Nieprawidłowy wiek")
elif wiek == 0 :
    print("Niemowlę")
elif wiek < 18 :
    print("Dziecko")
elif wiek >= 18 and wiek <= 120 :
    print("Dorosły")
elif wiek > 120 :
    print("Ludzie tyle nie żyją")