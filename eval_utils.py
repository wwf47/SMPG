from fractions import Fraction
def eval(order, pos):#(candidate, probability)
    prec30 = 0
    prec60 = 0
    prec90 = 0
    P30 = 0
    P60 = 0
    P90 = 0
    order_set = set()
    for c, p in order:#candidate, probability
        if p > 0:
            order_set.add(c)
    for i in range(30):
        if order[i][0] in pos:
            prec30 += 1
            P30 = Fraction(prec30, (i+1))+P30
    if prec30 == 0:
        AP30 = 0
    else:
        AP30 = P30/prec30
    for i in range(30,60):
        if order[i][0] in pos:
            prec60 += 1
            P60 = Fraction(prec60+prec30, (i+1))+P60
    prec60 += prec30
    if prec60 == 0:
        AP60 = 0
    else:
        AP60 = (P60+P30)/prec60
    for i in range(60,90):
        if order[i][0] in pos:
            prec90 += 1
            P90 = Fraction(prec90+prec60+prec30, (i+1))+P90
    prec90 += prec60
    if prec90 == 0:
        AP90 = 0
    else:
        AP90 = (P90+P60+P30)/prec90
    MAP = (AP30+AP60+AP90)/3

    prec30 /= float(30)
    prec60 /= float(60)
    prec90 /= float(90)

    return prec30, prec60, prec90, MAP, order_set




