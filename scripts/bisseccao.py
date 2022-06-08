def Bisseccao(f,a,b,E,param):
    erro= (b-a)/2
    p = (a+b)/2
    while erro>E:
        if f(p,param)*f(a,param)<0:
            b=p
        else:
            a=p
        erro= (b-a)/2
        p = (a+b)/2
    return p