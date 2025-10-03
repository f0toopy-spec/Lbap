result1=0
result=0
result2=0
result3=0
numbers = int(input('ведите число '))
while numbers != 0:
    result+=numbers
    numbers = int(input('ведите число '))
print('сумма введённых чисел ',result)
numbers = int(input('ведите число '))
while numbers >= 0:
    result1 += numbers
    numbers = int(input('ведите число '))
print('сумма введённых чисел ',result1)
numbers = int(input('ведите число '))
while numbers%2!=0:
    result2 += numbers
    numbers = int(input('ведите число '))
print('сумма введённых чисел ',result2)
numbers = int(input('ведите число '))
while numbers<=100:
    result3 += numbers
    numbers = int(input('ведите число '))
print('сумма введённых чисел ',result3)