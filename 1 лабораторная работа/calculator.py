number1 = int(input('Введите первое число: '))
number2 = int(input('Введите второе число: '))

if number1 == number2:
    print('числа равны')
else:
 print('большее число ', max(number1,number2))
 print('меньшее число ', min(number1, number2))
result = abs(number1 - number2)
print('Разница между числами:', result)