def get_free_land(s, g):
        
    S = s[0] * 100
    SG = g[0] * g[1]
    
    if S <= 0:
        raise ValueError('Не задана площадь участка')

    if SG <= 0:
        raise ValueError('Не задана площадь грядки')

    if SG > S:
        raise ValueError('Размер грядки больше размера участка')
 
    return S % SG
