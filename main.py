from budget import Category, create_spend_chart

categories = {}

def create_category():
    name = input("Enter category name: ")
    categories[name] = Category(name)

def deposit_money():
    name = input("Category: ")
    amount = float(input("Amount: "))
    categories[name].deposit(amount)

def withdraw_money():
    name = input("Category: ")
    amount = float(input("Amount: "))
    categories[name].withdraw(amount)

def show_chart():
    print(create_spend_chart(categories.values()))

while True:
    print("\n1. Create Category\n2. Deposit\n3. Withdraw\n4. Chart\n5. Exit")
    choice = input("Choose: ")

    if choice == "1":
        create_category()
    elif choice == "2":
        deposit_money()
    elif choice == "3":
        withdraw_money()
    elif choice == "4":
        show_chart()
    elif choice == "5":
        break
