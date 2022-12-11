from tabulate import tabulate


class Shoe:
    """'Shoe' class with its arguments and methods"""
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return float(self.cost)

    def get_quantity(self):
        return int(self.quantity)

    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


shoes_list = []  # The list will be used to store a list of objects of shoes.


def write_shoes_data():
    """use the array to write the file"""
    with open('inventory.txt', 'w', encoding='utf=-8') as file:
        file.write("Country,Code,Product,Cost,Quantity")
        for shoe in shoes_list:
            file.write("\n" + str(shoe))


def read_shoes_data():
    """it tries to read the file and insert the shoes in the array, if it cannot find the file or the
    file is not different from expected, it will report an error message."""
    try:
        with open('inventory.txt', 'r', encoding='utf=-8') as file:
            content_inventory = file.read().split("\n")[1:]  # skipping the first line when reading the file
        for shoe in content_inventory:
            shoe = shoe.split(",")
            shoes_list.append(Shoe(shoe[0], shoe[1], shoe[2], shoe[3], shoe[4]))
    except FileNotFoundError:
        print("File not found.")
    except IndexError:
        print("File failure!")


def print_shoes_tabulate(table):
    """receives the models of shoes that must be printed and print them using the 'tabulate'
    the 'value' column will only be shown if it has a value in the 'table' that it receives as an argument."""
    print(tabulate(table, headers=["Country", "Code", "Product", "Cost", "Quantity", "Value"]))


def capture_shoes():
    """receives data from a shoe, creates the object and adds it to the array
    and check if values for cost and quantity are valid"""
    country = input("Enter the country: ")
    code = input("Enter the code: ")
    product = input("Enter the product: ")
    while True:
        try:
            cost = float(input("Enter the cost: "))
            break
        except ValueError:
            print("Cost invalid, try again!")
    while True:
        try:
            quantity = int(input("Enter the quantity: "))
            break
        except ValueError:
            print("Quantity invalid, try again!")

    shoes_list.append(Shoe(country, code, product, cost, quantity))


def view_all():
    """creates the list 'table' runs through the array generating the table with the data received
    from '__str__' and at the end prints using the 'tabulate'."""
    table = []
    for shoe in shoes_list:
        table.append(str(shoe).split(","))
    print_shoes_tabulate(table)


def re_stock():
    """I created the 'low_stock' array to receive the quantities as 'int' to find out the index of the lowest stock,
    I print the model that has the lowest stock and ask how many you want to add from this model to replenish the stock,
    finally it saves the updated data in the file calling the 'write_shoes_data' function."""
    low_stock = []
    for shoe in shoes_list:
        low_stock.append(shoe.get_quantity())
    print_shoes_tabulate([str(shoes_list[low_stock.index(min(low_stock))]).split(",")])

    shoes_list[low_stock.index(min(low_stock))].quantity = \
        str(int(input("How many do you want to add from this shoe? ")) + min(low_stock))

    write_shoes_data()


def search_shoe():
    """it goes through the array looking for the given code, it prints the corresponding shoe if it finds it."""
    researched = input("Enter the code to search: ")
    for shoe in shoes_list:
        if shoe.code == researched:
            print_shoes_tabulate([str(shoe).split(",")])
            break


def value_per_item():
    """I used list comprehension to generate a list with one more column and send it as an argument in
    the 'print_shoes_tabulate' function that will print using tabulate."""
    print_shoes_tabulate([str(shoe).split(",") + [shoe.get_quantity() * shoe.get_cost()] for shoe in shoes_list])


def highest_qty():
    """I created the 'highest_stock' array to receive the quantities to find out the index of the highest stock,
    I print the model that has the highest stock using this index"""
    highest_stock = []
    for shoe in shoes_list:
        highest_stock.append(shoe.get_quantity())
    print_shoes_tabulate([str(shoes_list[highest_stock.index(max(highest_stock))]).split(",")])
    print("This shoe as being for sale.")


# ==========Main Menu=============
"""Program execution starts by loading data from the file into memory and 
then a looping menu to navigate between functions."""
read_shoes_data()
menu = ""
while menu != "quit":
    menu = input('''\tMenu:
    Add - To add a new model
    All - To view all models
    Low - To add quantity to lower stock
    Srh - To search a model by code
    Api - To see the total amount per item in stock
    Hig - To see the model with the largest quantity in stock\n
    Quit - To exit.
    \tWhat would you like to do? ''').lower()

    if menu == "add":
        capture_shoes()
        write_shoes_data()
    elif menu == "all":
        view_all()
    elif menu == "low":
        re_stock()
    elif menu == "srh":
        search_shoe()
    elif menu == "api":
        value_per_item()
    elif menu == "hig":
        highest_qty()
    elif menu == "quit":
        print("Goodbye, See ya..")
    else:
        print("Invalid option! Try again!")
