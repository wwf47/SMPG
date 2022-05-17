from fractions import Fraction


def eval_can(order, pos):  # (candidate, probability)
    pre30 = 0
    pre60 = 0
    pre90 = 0
    p30 = 0
    p60 = 0
    p90 = 0
    order_set = set()
    for c, p in order:  # candidate, probability
        if p > 0:
            order_set.add(c)
    for i in range(30):
        if order[i][0] in pos:
            pre30 += 1  # correct
            p30 = Fraction(pre30, (i+1))+p30  # pre@i
    if pre30 == 0:
        ap30 = 0
    else:
        ap30 = p30/pre30  # sum of pre@i\correct instances
    for i in range(30,60):
        if order[i][0] in pos:
            pre60 += 1
            p60 = Fraction(pre60+pre30, (i+1))+p60
    pre60 += pre30
    if pre60 == 0:
        ap60 = 0
    else:
        ap60 = (p60+p30)/pre60
    for i in range(60,90):
        if order[i][0] in pos:
            pre90 += 1
            p90 = Fraction(pre90+pre60+pre30, (i+1))+p90
    pre90 += pre60
    if pre90 == 0:
        ap90 = 0
    else:
        ap90 = (p90+p60+p30)/pre90
    maps = (ap30+ap60+ap90)/3

    pre30 /= float(30)  # pre@30/num
    pre60 /= float(60)
    pre90 /= float(90)

    return pre30, pre60, pre90, maps, order_set




