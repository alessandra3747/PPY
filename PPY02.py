#ZADANIE 1
student_results = [{"Ania" : [101, 75, 33]}, {"Kasia" : [76, 55, 12]}, {"Bartek" : [65, 55, 60]}, {"Marek" : [23, 80, 98]}]

for record in student_results:
    for grades in record.values():
        for grade in grades:
            if grade > 100:
                grades.remove(grade)


average_score = {}

for record in student_results:
    for name, grades in record.items():
        sum = 0
        for grade in grades:
            sum += grade
    average_score[name] = sum/len(grades)


best_student = ["" , 0]
for name, avg in average_score.items():
    if best_student[1] < avg:
        best_student[0] = name
        best_student[1] = avg


print("Najwyższą średnią uzyskał/ła " + best_student[0] + " , która wynosiła " + str(best_student[1]))


#ZADANIE 2
s = 'one'
lista = ['one', 'two', 'none', 'three', 'neon', 'eon']

s_chars = set(s)

for element in lista:
    element_chars = set(element)
    if element_chars == s_chars and element != s:
        print(element)


print()


#ZADANIE 3
ksiazka_adresowa = dict()

print("Aby zakończyć działanie programu wpisz X")
print("Aby zdodać nowy kontakt do książki adresowej wpisz +")
print("Aby wyświetlić wszystkie kontakty w książce adresowej wpisz #")
print("Aby wyszukać kontakt w książce adresowej wpisz ?")
print("Aby usunąć kontakt z książki adresowej wpisz -")
user_input = ""

while user_input != "X":
    user_input = input()
    match user_input:
        case "+":
            print("Dodawanie nowego kontaktu, wpisz nazwe kontaktu: ")
            name = input()
            print("Wpisz informacje o kontakcie: ")
            ksiazka_adresowa[name] = input()
            print("Dodano nowy kontakt")
        case "#":
            for imie, informacje in ksiazka_adresowa.items():
                print(imie + " " + informacje)
        case "?":
            print("Podaj nazwe wyszukiwanego kontaktu: ")
            print(ksiazka_adresowa[input()])
        case "-":
            print("Podaj nazwe usuwanego kontaktu: ")
            ksiazka_adresowa.pop(input())
            print("Usunieto kontakt")



#DODATKOWE
apple = [4,5,7]
capacity = [6,4,10,3]

sum_apple = 0
for i in apple:
    sum_apple += i

capacity.sort()
capacity.reverse()



print(capacity)
print(sum_apple)

capacity_sum = 0
result = 0

for i in capacity:
    capacity_sum += i
    result += 1
    if capacity_sum >= sum_apple:
        print(result)
        break
