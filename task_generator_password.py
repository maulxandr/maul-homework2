import random  
import string

def password_generator(n):
    while 1:
        pas = []
        for i in range(n):
            pas.append(random.choice(string.ascii_letters))
        yield ''.join(pas)
