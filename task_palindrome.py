def is_palindrome(s):
    s = str(s)
    s = s.lower().replace(' ', '').replace(',', '').replace('.','').replace('!','').replace('?','')
    rev_s = ''.join(reversed(s))

    return s == rev_s
