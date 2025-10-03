result=0
result1=0
result2=0
result3=0
number=int(input('ведите число N '))
for i in range(1,number+1):
    result+=i
    if i%2==0:
        result2+=i
    else:
        result3+=i
for i in range(1,11):
    result1+=i
print('сумма чисел от 1 до 10 ',result1)
print('сумма чисел от 1 до N ',result)
print('сумма чётных чисел от 1 до N ',result2)
print('сумма нечётных чисел от 1 до N ',result3)