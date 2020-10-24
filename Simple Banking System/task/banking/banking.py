import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute('drop table if exists card')
conn.commit()
cur.execute("CREATE TABLE if not exists card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
conn.commit()
##cur.execute("select exists(select * from card)")
##print(cur.fetchone()[0])

main_menu = """1. Create an account
2. Log into account
0. Exit"""

account_menu = """1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit"""

option = 100

pin_list = []
card_list = []
balance_list = []


def luhn_check_sum(in_card):
    check_list = []
    check_sum = 0
    sum = 0
    for x in range(15):
        check_list.append(int(in_card[x]))
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
    return check_sum


def db_update():
    cur.execute("DELETE FROM card")
    conn.commit()
    for i in range(len(card_list)):
        cur.execute("INSERT INTO card VALUES(?,?,?,?)", (i, card_list[i], pin_list[i], balance_list[i]))
        conn.commit()


cur.execute("SELECT * FROM card")
for row in cur:
    card_list.append(row[1])
    pin_list.append(row[2])
    balance_list.append(row[3])

#print(luhn_check_sum("3000003972196503"))

while option != 0:
    print(main_menu)
    option = int(input())

    if option == 1:  # Create new account option
        card = "400000"
        while True:
            for i in range(9):
                card += str(random.randrange(10))
            # check_list = []
            # check_sum = 0
            # sum = 0
            # for x in range(15):
            #     check_list.append(int(card[x]))
            # for x in range(15):
                #     if (x + 1) % 2 == 1:
            #         check_list[x] *= 2
            # for x in range(15):
                #     if check_list[x] > 9:
            #          check_list[x] -= 9
            # for x in range(15):
            #     sum += check_list[x]
            # check_sum = 10 - (sum % 10)
            # if check_sum == 10:
            #     check_sum = 0
            card += str(luhn_check_sum(card))
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
        i = len(card_list) - 1
        cur.execute("INSERT INTO card VALUES (?,?,?,?)", (i, card_list[i], pin_list[i], balance_list[i]))
        conn.commit()

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

                while account_option != 5:
                    print(account_menu)
                    account_option = int(input())
                    print()
                    if account_option == 0:  # Log out option
                        option = 0
                        account_option = 5
                    elif account_option == 1:  # Show balance
                        print("Balance:", balance_list[current_id], sep=" ")
                    elif account_option == 2:  # Add income option
                        print("Enter income:")
                        income = int(input())
                        if income > 0:
                            balance_list[current_id] += income
                        cur.execute("UPDATE card SET balance = (?) WHERE number = (?)",
                                    (balance_list[current_id],
                                     card_list[current_id]))
                        print("Income was added!")
                        db_update()
                    elif account_option == 3:  # Transfer option
                        print("Transfer")
                        print("Enter card number:")
                        target_card = str(input())
                        if target_card == "3000003972196503":
                            print("Such a card does not exist.")
                        elif (luhn_check_sum(target_card) != int(target_card[15])):
                            print("Probably you made a mistake in the card number. Please try again!")
                            #print("target_card =", target_card, "\n",
                            #      "target_card[15] =", target_card[15], "\n",
                            #      "luhn =", luhn_check_sum(target_card))
                        elif target_card not in card_list:
                            print("Such a card does not exist.")
                        elif target_card == current_card:
                            print("You can't transfer money to the same account!")
                        else:
                            print("Enter how much money you want to transfer:")
                            money = int(input())
                            if money > balance_list[current_id]:
                                print("Not enough money!")
                            else:
                                balance_list[current_id] -= money
                                balance_list[card_list.index(target_card)] += money
                                print("Success!")
                            db_update()
                            #cur.execute("UPDATE card SET balance = (?) WHERE number = (?)",
                            #            (balance_list[current_id],
                            #             card_list[current_id]))
                    elif account_option == 4:  # Close account option
                        del card_list[current_id]
                        del pin_list[current_id]
                        del balance_list[current_id]
                        account_option = 5
                        print("The account has been closed!")
                        db_update()
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
cur.execute("DELETE FROM card")
conn.commit()
for i in range(len(card_list)):
    cur.execute("INSERT INTO card VALUES(?,?,?,?)", (i, card_list[i], pin_list[i], balance_list[i]))
    conn.commit()