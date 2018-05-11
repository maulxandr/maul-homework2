AX = int(input())
AY = int(input())
BX = int(input())
BY = int(input())
CX = int(input())
CY = int(input())

# Вычислим длины сторон треугольника
AB = ((AX - BX) ** 2 + (AY - BY) ** 2) ** 0.5
BC = ((BX - CX) ** 2 + (BY - CY) ** 2) ** 0.5
AC = ((AX - CX) ** 2 + (AY - CY) ** 2) ** 0.5

# Выполним проверку, является ли треугольник прямоугольным
if AB ** 2 == BC ** 2 + AC ** 2:
    print('yes')
elif BC ** 2 == AB ** 2 + AC ** 2:
    print('yes')
elif AC ** 2 == AB ** 2 + BC ** 2:
    print('yes')
else:
    print('no')
