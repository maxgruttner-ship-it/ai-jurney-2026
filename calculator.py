def main():
    x = int(input("Was ist x? "))
    print("x quadriert ergibt", square(x))

def square(n):
    return n ** 2

main()