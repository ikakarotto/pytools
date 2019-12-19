#!/usr/bin/env python2.7
import random

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

