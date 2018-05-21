n = int(input())
p = int(input())


with open('data.txt') as f:
    i = f.readline().split(' ')
    

with open('out-1.txt', 'w') as f:
    for a in i:
        if int(a) % n == 0:
            f.write(str(a) + ' ')


with open ('out-2.txt', 'w') as f:
    for a in i:
        f.write(str(int(a) ** p) + ' ')



