# a = 'ABCABBA' # to string
# b = 'CBABAC' # from string
a = 'CBABAC'
b = 'ABCABBA'

# a row, b column
# a x b
# row order
m = [ [0 for _ in range(len(b)+1)] for _ in range(len(a)+1)]

# LCS table
for i in range(1, len(a)+1):
    for j in range(1, len(b)+1):
        if a[i-1] == b[j-1]:
            m[i][j] = m[i-1][j-1] + 1
        else:
            m[i][j] = max(m[i][j-1], m[i-1][j])

for line in m:
    print(' '.join(map(str, line)))
print()

start = (len(a), len(b))
pos = start
ops = []
n = [ [ 0 for _ in range(len(b)+1)] for _ in range(len(a)+1)]

# find a path
while any(pos):
    i = pos[0]
    j = pos[1]
    print(i, j)
    n[i][j] = m[i][j]
    
    if i >= 0 and m[i][j-1] == m[i][j]:
        pos = (i, j-1)
        ops.append('-'+b[j-1])
    elif j >= 0 and m[i-1][j] == m[i][j]:
        pos = (i-1, j)
        ops.append('+'+a[i-1])
    else:
        pos = (i-1, j-1)
        ops.append('='+a[i-1])

for line in n:
    print(' '.join(map(str, line)))
print()

# need to reverse
ops.reverse()
print(ops)

# test
t = b
i=0
result = []
for op in ops:
    match op[0]:
        case '+':
            t = t[:i]+op[1]+t[i:]
            i+=1
            result.append('\033[32m'+op[1]+'\033[0m')
        case '-':
            t = t[:i]+t[i+1:]
            result.append('\033[31m'+op[1]+'\033[0m')
        case '=':
            i+=1
            result.append(op[1])
print(b)
print(a)
print(t)
print(''.join(result))
