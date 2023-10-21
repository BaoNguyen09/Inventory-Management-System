def user_interface(): # this function print out the menu
    print("------------------------------------------------")
    print("Welcome to Bao's Inventory Management System !!!")
    print("------------------------------------------------")
    print("Here is the menu:")
    print("1. List products")
    print("2. Add products")
    print("3. Update price")
    print("4. Remove products")
    print("5. Sell products")
    print("6. Restock products")
    print("7. Search products")
    print("8. Generate Sales Report")
    print("9. Generate Low Stock Report")
    print("10. Menu")
    print("11. Exit\n")


def open_inventory():
    # this function will open the file storing every product
    # and transfer that into a dictionary for later usage
    file = open('warehouse.txt')
    storage_dict = {}
    for line in file:
        if line.strip(): # check if the line is empty
            line = line.strip("\n").split(" ") # remove the new line character and put every character into a list
            key = (line[0],line[1])
            product_info = [int(line[2]),int(line[3])] # I change the type of price and quantity to int for easier calculation
            storage_dict[key] = product_info
    file.close()
    return storage_dict


def listing(storage_dict):
    # this function simply print out a list of products in the warehouse
    print("-----------------------------------------------")
    print("ID           Name         Price        Quantity")
    print("-----------------------------------------------")
    
    for key in storage_dict:
        product_info = storage_dict[key]
        ID = padded(key[0])
        name = padded(key[1])
        price = padded(product_info[0])
        quantity = padded(product_info[1])
        print("{0}{1}{2}{3}".format(ID, name, price, quantity))


def padded(string): 
    # this function take in a string and return a string with a number of spaces
    new_string = str(string)
    for i in range(13 - len(str(string))):
        new_string += " "
    return new_string
    

def adding(storage_dict):
    # this function as for basic info of product 
    # and use those info to add product into the dictionary
    ID = input("What is the ID of this product? ")
    Name = input("What is the product's name? ")
    Price = int(input("What is the price? "))
    Quantity = int(input("How many products to add? "))
    storage_dict [(ID, Name)] = [Price, Quantity]
    return storage_dict


def update_price(storage_dict):
    # this function as for the product's name or ID to search 
    # the product and then ask the new price to update
    ID = input("Enter the ID or name of product: ")
    for key in storage_dict:
        if key[0] == ID or key[1] == ID: # check if the name or ID is correct
            price = int(input("Enter new price: "))
            storage_dict[key][0] = price
            return storage_dict
    print("This product is not in the current list!")


def remove(storage_dict):
    # this function ask for the name or ID of product to remove
    # if the product is not in the shop it will print out a notice
    name = input("Enter the name or ID of the product to remove: ")
    for key in storage_dict:
        if key[0] == name or key[1] == name: # check if the product is in the shop
            del storage_dict[key]
            return storage_dict
    print("This product is not yet in the list!")


def restock(storage_dict):
    # this function asks for the product identity and then restock them
    ID = input("Enter the ID or name of product: ")
    for key in storage_dict:
        if key[0] == ID or key[1] == ID:
            number = int(input("Enter number to restock: "))
            original_number = storage_dict[key][1] # create variable for the current number of products
            storage_dict[key][1] = original_number + number # add restock number to the product
            return storage_dict
    print("This product is not in the current list!")


def search(storage_dict):
    # this function search a product according to its name and ID
    name = input("Enter name or ID of product: ")
    for key in storage_dict:
        if key[0] == name or key[1] == name:
            search_dict = {}
            search_dict[key] = storage_dict[key]
            return listing(search_dict)
    print("This product is not in the current list!")


def sell(storage_dict):
    # this function create a new dictionary of products that customers buy
    # it makes permanent changes to the storing dictionary
    answer = "yes" 
    customer_cart = {}
    while answer == "yes":
        ID = input("Enter name or ID of product you want to buy: ")
        for key in storage_dict:
            if key[0] == ID or key[1] == ID: # search a product
                stock = storage_dict[key][1] # current number of products in the shop
                number = int(input("Enter number of products you want to buy: "))
                if stock >= number and stock > 0: # check if the products is out of stock or people buy more than we have
                    price = storage_dict[key][0]
                    if key not in customer_cart.keys(): # if the products has not been in the customer's cart
                        number = number 
                    else: # if the products has been in customer's cart
                        number = customer_cart[key][1] + number
                    total = number * price
                    product_info = [price, number, total]
                    customer_cart[key] = product_info
                    storage_dict[key][1] = stock - number # update number of products into the system
                    found = True # use this to check if a product is found
                else: # if the products is out of stock
                    print("This product is currently out of stock. Choose another one, please!")
        if not found: # check if the product is not found
            print("This product is not in our shop")
        answer = input("Do you want to continue shopping (yes or no)? ")
        print()
    answer = input("Do you want a receipt (yes or no)? ")
    if answer == "yes": # make a text file for customer's receipt as well as print it out.
        receipt(customer_cart) # call out another function to store current customer's receipt
        file = open('receipt.txt')
        print(file.read())
        file.close()
    else:
        open('receipt.txt',"wt").close() 
        # delete the receipt of previous customer
    store_receipt(customer_cart) # call out another function to store all receipts for sale report
    return storage_dict


def receipt(customer_cart):
    # this function store the current customer's receipt to a text file
    file = open('receipt.txt',"wt")
    sum = 0
    index = 1
    file.write(
'''----------------------------------------------------------------------
Index        ID           Name         Price        Quantity     Total
----------------------------------------------------------------------\n''')
    for key in customer_cart:  
        ID = padded(key[0]) 
        name = padded(key[1])
        price = customer_cart[key][0]
        quantity = customer_cart[key][1]
        total = price * quantity
        file.write("{0}{1}{2}{3}{4}{5}\n".format(padded(index), ID, name, padded(price), padded(quantity), total))
        index += 1
        sum += total
    file.write("----------------------------------------------------------------------\n")
    file.write("The total money to pay is: {0}".format(sum))
    file.close()


def store_receipt(customer_cart):
    # this function store all receipts into a text file for sale report
    file = open('store_receipt.txt',"at")
    sum = 0
    for key in customer_cart: 
        ID = key[0]  
        name = key[1]
        price = customer_cart[key][0]
        quantity = customer_cart[key][1]
        file.write("{0} {1} {2} {3}\n\n".format(ID, name, price, quantity))
    file.close()


def sale_report():
    # this function generate sale report from all the receipts 
    file = open('store_receipt.txt')
    report_dict = {}
    for line in file:
        if line.strip(): # check if a line is empty
            line = line.strip("\n").split(" ") # create a list of each info of the product
            key = (line[0],line[1])
            if key not in report_dict.keys(): # if a product is not in the report, it will create one
                value = [int(line[2]),int(line[3])]
                report_dict[key] = value
            else: # if the product is already in the report, it will just add up the number
                old_quantity = report_dict[key][1]
                new_quantity = int(line[3])
                report_dict[key][1] = old_quantity + new_quantity
    file.close()
    # transfer the info in the dictionary above to a text file
    file = open('sale report.txt',"at")
    file.write('''
------------------------------------------------------------
Index        ID           Name         Price        Quantity
------------------------------------------------------------
\n''')
    sum = 0
    index = 1
    for key in report_dict: 
        ID = padded(key[0])  
        name = padded(key[1])
        price = report_dict[key][0]
        quantity = report_dict[key][1]
        total = price * quantity
        file.write("{0}{1}{2}{3}{4}\n".format(padded(index), ID, name, padded(price), padded(quantity)))
        index += 1
        sum += total
    file.write("The total profit this time is: {0}\n\n".format(sum))
    file.close()
    # print out the report
    file = open('sale report.txt')
    print(file.read())


def low_stock(storage_dict):
    # this function will print out a list of low-in-stock products(less than or equal 5)
    low_stock_dict = {}
    for key in storage_dict:
        quantity = storage_dict[key][1]
        if quantity <= 5: # check the quantity and store them into another dictionary
            low_stock_dict[key] = storage_dict[key]
    if low_stock_dict != {}: # if the list is not empty
        print("Here is the list of low stock item")
        listing(low_stock_dict)
    else:
        print("There is no low stock items.")


def close_inventory(storage_dict):
    # this function transfers all item in the storing dictionary into a text file called warehouse
    file = open('warehouse.txt',"wt") 
    # I overwrite them so that I don't have to check if a product has already been in the warehouse
    for key in storage_dict:
        ID = key[0]
        Name = key[1]
        Price = str(storage_dict[key][0])
        Quantity = str(storage_dict[key][1])
        file.write(ID + " " + Name + " " + Price + " " + Quantity + "\n")
    file.close()


def main():
    # this function combines all functions to create an interactive program
    user_interface()
    storage_dict = open_inventory()
    choice = 0.1
    while choice > 0 and choice <= 11:
        choice = int(input("What is your choice? "))
        if choice == 1:
            listing(storage_dict)
        elif choice == 2:
            adding(storage_dict)
        elif choice == 3:
            update_price(storage_dict)
        elif choice == 4:
            remove(storage_dict)
        elif choice == 5:
            sell(storage_dict)
        elif choice == 6:
            restock(storage_dict)
        elif choice == 7:
            search(storage_dict)
        elif choice == 8:
            sale_report()
        elif choice == 9:
            low_stock(storage_dict)
        elif choice == 11:
            break
        elif choice == 10:
            user_interface()
        else: # this is to handle if a choice is not valid
            user_interface()
            choice = 0.1
            continue
        print()
    print("Thank you for visiting !!!")
    close_inventory(storage_dict)
main()
