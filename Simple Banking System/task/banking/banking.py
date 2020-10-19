import random

main_menu = """1. Create an account
2. Log into account
0. Exit"""

option = 100

while option != 0:  # Create new account option
    print(main_menu)
    option = int(input())

    if option == 1:
        card = "400000"
        for i in range(10):
            card += str(random.randrange(10))
        PIN = ""
        for i in range(4):
            PIN += str(random.randrange(10))
        print()
        print("Your card has been created")
        print("Your card number:")
        print(card)
        print("Your card PIN:")
        print(PIN)
        print()

    elif option == 2:  # Log into account option
        pass

print()
print("Bye!")