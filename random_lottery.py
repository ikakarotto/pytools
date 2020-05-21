#!/usr/bin/env python
# Description: 大概是用来做36选7叭
import random
import sys

pyver = sys.version_info.major

if pyver == 2:
    pass
elif pyver == 3:
    from functools import reduce
else:
    sys.exit(1)

lottery_list = []
while len(lottery_list) < 7:
    lottery_list.append((random.randint(1,33)))
    func = lambda x,y:x if y in x else x + [y]
    lottery_list = reduce(func, [[], ] + lottery_list)

# print(lottery_list)

random_index = random.randint(0,6)
print(lottery_list[random_index])

lottery_list.pop(random_index)
lottery_list.sort()
print(lottery_list)

# N=random.randint(a,b)
# a <= N <= b
