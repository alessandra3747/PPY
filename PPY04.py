#ZADANIE 1

def kalkulator(*args, **kwargs):
   result = args[0]

   i = 1
   for dzialanie in kwargs:

       match kwargs[dzialanie]:
        case '+':
            result += args[i]
        case '-':
            result -= args[i]
        case '*':
            result *= args[i]
        case '/':
            result /= args[i]

       i += 1

   return result


print(kalkulator(1,3,2,działanie_1='+',działanie_2="-"))


#ZADANIE 2

def calculate_statistics(typ_operacji, *args):
    if(typ_operacji == "mean"):
        return sum(args)/len(args)

    if(typ_operacji == "median"):
        if len(args) % 2 == 0:
            return (sorted(args)[len(args)//2 - 1] + sorted(args)[len(args)//2] ) / 2
        else:
            return sorted(args)[len(args)//2]

    if(typ_operacji == "mode"):

        wystapienia_liczb = dict()

        for i in range(len(args)):
            if wystapienia_liczb.get(args[i]) is None:
                wystapienia_liczb[args[i]] = 1
            else:
                wystapienia_liczb[args[i]] += 1

        max_count = max(wystapienia_liczb.values())
        result = []
        for x,y in wystapienia_liczb.items():
            if y == max_count:
                result.append(x)
        return result


print(calculate_statistics("mean", 1, 2, 3, 4, 5))  # 3.0
print(calculate_statistics("median", 1, 2, 3, 4, 5))  # 3
print(calculate_statistics("mode", 1, 2, 2, 3, 3, 3))  # [3]


#ZADANIE 3

def validate_pesel(pesel):
    if len(pesel) != 11 :
        return False

    wagi = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]

    suma_kontrolna = sum(int(pesel[i]) * wagi[i] for i in range(10))

    cyfra_kontrolna = 10 - (suma_kontrolna % 10) % 10

    return cyfra_kontrolna == int(pesel[-1])


print(validate_pesel('12345678901')) # False
print(validate_pesel('44051401458')) # True



#ZADANIE FANG
def trzyelementowe_grupy(*args):
    result = set()
    n = len(args)

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if args[i] + args[j] + args[k] == 0:
                    trójka = tuple(sorted([args[i], args[j], args[k]]))
                    result.add(trójka)

    return list(result)


print(trzyelementowe_grupy(1, -1, -1, 0, 2))