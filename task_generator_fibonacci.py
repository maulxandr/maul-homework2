def fibonacci(n):
    fib1 = 0
    fib2 = 1
    for i in range(n):
        fib1, fib2 = fib2, fib1 + fib2
        yield fib1

