a = 'ABCABBA' # to string
b = 'CBABAC' # from string

import os
from collections import namedtuple
import sys
import time

# to store results
Keep = namedtuple('Keep', ['char'])
Keep.__repr__ = lambda self: self.char
Insert = namedtuple('Insert', ['char'])
Insert.__repr__ = lambda self: '+'+self.char
Remove = namedtuple('Remove', ['char'])
Remove.__repr__ = lambda self: '-'+self.char

Frontier = namedtuple('Frontier', ['x', 'history'])

n = [ [ '_' for _ in range(len(b)+1)] for _ in range(len(a)+1)]

def print_step(d, k, x, y, frontier):
    os.system('clear -x')
    print(b, '->', a)
    l = list(frontier.keys())
    l.sort()
    print('   ', ' '.join(b))
    aa = ' '+a+' '
    for i, line in enumerate(n):
        print(aa[i], ' '.join(map(str, line)))
    print()
    print('Steps:')
    for k in l:
        print(' ', k, frontier[k])
    time.sleep(0.5)

dest = lambda f: sum(map(lambda it:not isinstance(it, Keep), f))

def myers_diff(b, a):
    # paths
    frontier = {1: Frontier(0, [])}

    def one(idx):
        return idx - 1

    a_max = len(a)
    b_max = len(b)
    n[0][0] = 0
    for d in range(0, a_max + b_max + 1):
        # why step 2?
        # https://chuquan.me/2023/09/13/myers-difference-algorithm/#myers-%E5%B7%AE%E5%88%86%E7%AE%97%E6%B3%95
        # "内层循环：迭代必要的 K 值。对于每一条 K 线，从其上的最佳位置出发，移动深度加 1 后
        # 的位置只能在其相邻的两条 K 线上。因此，相同深度的最佳位置所在的 K 线，相邻之间的 K
        # 值差为2。对应地，内层循环的步长也为2，并且每一轮遍历，深度加1，K的范围也会外扩2。"
        for k in range(-d, d + 1, 2):
            # if k != -d and k != d then k+-1 exists
            # k + 1 means insertation, k - 1 means deletation
            # k means same, and shouldn't be procceed here
            go_down = (k == -d or 
                    (k != d and frontier[k - 1].x < frontier[k + 1].x))

            if go_down:
                # keep x and increase y because y = x - k and ?
                x, history = frontier[k + 1]
            else:
                # increase x and keep y
                x, history = frontier[k - 1]
                x += 1

            history = history[:]
            y = x - k

            if 1 <= y <= b_max and go_down:
                # go_down means insertation
                history.append(Insert(b[one(y)]))
                n[y][x] = dest(history)
            elif 1 <= x <= a_max and y <= b_max:
                # else means deletation
                history.append(Remove(a[one(x)]))
                n[y][x] = dest(history)

            while x < a_max and y < b_max and a[one(x + 1)] == b[one(y + 1)]:
                # find all same elements
                x += 1
                y += 1
                history.append(Keep(a[one(x)]))
                n[y][x] = dest(history)

            if x >= a_max and y >= b_max:
                frontier[k] = Frontier(x, history)
                print_step(d, k, x, y, frontier)
                return history
            else:
                frontier[k] = Frontier(x, history)
            print_step(d, k, x, y, frontier)

    assert False, 'Could not find edit script'

def main():
    diff = myers_diff(a, b)
    for elem in diff:
        if isinstance(elem, Keep):
            print(' ' + elem.char)
        elif isinstance(elem, Insert):
            print('+' + elem.char)
        else:
            print('-' + elem.char)

if __name__ == '__main__':
    sys.exit(main())
