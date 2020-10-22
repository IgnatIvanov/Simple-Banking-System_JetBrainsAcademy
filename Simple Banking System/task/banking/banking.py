import random

main_menu = """1. Create an account
2. Log into account
0. Exit"""

account_menu = """1. Balance
2. Log out
0. Exit"""

option = 100

pin_list = []
card_list = []
balance_list = []

while option != 0:
    print(main_menu)
    option = int(input())

    if option == 1:  # Create new account option
        card = "400000"
        while True:
            for i in range(9):
                card += str(random.randrange(10))
            check_list = []
            check_sum = 0
            sum = 0
            for x in range(15):
                check_list.append(int(card[x]))
            for x in range(15):
                if (x + 1) % 2 == 1:
                    check_list[x] *= 2
            for x in range(15):
                if check_list[x] > 9:
                    check_list[x] -= 9
            for x in range(15):
                sum += check_list[x]
            check_sum = 10 - (sum % 10)
            if check_sum == 10:
                check_sum = 0
            card += str(check_sum)
            if card not in card_list:
                break
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

        card_list.append(card)
        pin_list.append(PIN)
        balance_list.append(0)

    elif option == 2:  # Log into account option
        print()
        print("Enter your card number:")
        card = input()
        print("Enter your PIN:")
        PIN = input()
        print()

        if card in card_list:
            if pin_list[card_list.index(card)] == PIN:
                print("You have successfully logged in!")
                print()

                current_card = card
                current_id = card_list.index(current_card)
                account_option = 100

                while account_option != 2:
                    print(account_menu)
                    account_option = int(input())
                    print()
                    if account_option == 0:
                        option = 0
                        account_option = 2
                    elif account_option == 1:
                        print("Balance:", balance_list[current_id], sep=" ")
                    print()
                print("You have successfully logged out!")
                print()
            else:
                print("Wrong card number or PIN!")
                print()
        else:
            print("Wrong card number or PIN!")
            print()

print()
print("Bye!")