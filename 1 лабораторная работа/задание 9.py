num = str(input("введите символ "))
num2=str(1234567890)
num3='qwertyuiopasdfghjklzxcvbnmёйцукенгшщзхъэждлорпавыфячсмитьбюQWERTYUIOPASDFGHJKLZXCVBNMЁЙЦУКЕНГШЩЗХЪЭЖДЛОРПАВЫФЯЧСМИТЬБЮ'
num4='уеыаоэяиюёaeuoiyAEOUIYУЕЁЫАОЭЯИЮ'
num5='QWERTYUIOPASDFGHJKLZXCVBNMЁЙЦУКЕНГШЩЗХЪЭЖДЛОРПАВЫФЯЧСМИТЬБЮ'
if len(num)== 1:
 if num in num2:
    print('является числом')
 else:
     print('не является числом')
 if str(num) in num3:
    print('является буквой')
 else:
    print('не является буквой')
 if str(num) in num4:
    print('является гласной буквой')
 else:
     print('не является гласной буквой')
 if str(num) in num5:
    print('является прописной буквой')
 else:
    print('является строчной')
else:
    print('вы ввели не символ')