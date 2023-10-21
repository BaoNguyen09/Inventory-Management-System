def user_interface():
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
    # dict = {("ID","name") : ["price", "quantity"]}
    # return choice

def open_inventory():
    file = open("warehouse.txt")
    data_dict = {}
    for line in file:
        if line.strip():
            line = line.strip("\n").split(" ")
            key = (line[0],line[1])
            value = [line[2],line[3]]
            data_dict[key] = value
    file.close()
    return data_dict

def listing(data_dict):
    print("-----------------------------------------------")
    print("ID           Name         Price        Quantity")
    print("-----------------------------------------------")
    
    for key in data_dict:
        value = data_dict[key]
        ID = padded(key[0])
        name = padded(key[1])
        price = padded(value[0])
        quantity = padded(value[1])
        print("{0}{1}{2}{3}".format(ID, name, price, quantity))

def padded(string):
    new_string = str(string)
    for i in range(13 - len(str(string))):
        new_string += " "
    return new_string
    
def adding(data_dict):
    ID = input("What is the ID of this product? ")
    Name = input("What is the product's name? ")
    Price = int(input("What is the price? "))
    Quantity = int(input("How many products to add? "))
    data_dict [(ID, Name)] = [Price, Quantity]
    return data_dict

def update_price(data_dict):
    ID = input("Enter the ID or name of product: ")
    for key in data_dict:
        if key[0] == ID or key[1] == ID:
            price = int(input("Enter new price: "))
            data_dict[key][0] = price
            return data_dict
    print("This product is not in the current list!")

def remove(data_dict):
    name = input("Enter the name or ID of the product to remove: ")
    for key in data_dict:
        if key[0] == name or key[1] == name:
            del data_dict[key]
            return data_dict
    print("This product is not yet in the list!")

def restock(data_dict):
    ID = input("Enter the ID or name of product: ")
    for key in data_dict:
        if key[0] == ID or key[1] == ID:
            number = int(input("Enter number to restock: "))
            original_number = int (data_dict[key][1])
            data_dict[key][1] = original_number + number
            return data_dict
    print("This product is not in the current list!")

def search(data_dict):
    name = input("Enter name or ID of product: ")
    for key in data_dict:
        if key[0] == name or key[1] == name:
            new_dict = {}
            new_dict[key] = data_dict[key]
            return listing(new_dict)
    print("This product is not in the current list!")

def sell(data_dict):
    answer = "yes"
    new_dict = {}
    while answer == "yes":
        ID = input("Enter name or ID of product you want to buy: ")
        for key in data_dict:
            if key[0] == ID or key[1] == ID:
                stock = int(data_dict[key][1])
                number = int(input("Enter number of products you want to buy: "))
                if stock >= number and stock > 0:
                    price = int(data_dict[key][0])
                    if key not in new_dict.keys():
                        number= number 
                    else: 
                        number = new_dict[key][1] + number
                    total = number * price
                    value = [price, number, total]
                    new_dict[key] = value
                    data_dict[key][1] = stock - number
                    found = True
                else:
                    print("This product is currently out of stock. Choose another one, please!")
        if not found:
            print("This product is not in the list")
        answer = input("Do you want to continue shopping (yes or no)? ")
        print()
    answer = input("Do you want a receipt (yes or no)? ")
    if answer == "yes":
        receipt(new_dict)
        file = open("receipt.txt")
        print(file.read())
        file.close()
    else:
        open("receipt.txt","wt").close()
    store_receipt(new_dict)
    return data_dict
def receipt(new_dict):
    file = open("receipt.txt","wt")
    sum = 0
    index = 1
    file.write(
'''----------------------------------------------------------------------
Index        ID           Name         Price        Quantity     Total
----------------------------------------------------------------------\n''')
    for key in new_dict:  
        ID = padded(key[0]) 
        name = padded(key[1])
        price = new_dict[key][0]
        quantity = new_dict[key][1]
        total = price * quantity
        file.write("{0}{1}{2}{3}{4}{5}\n".format(padded(index), ID, name, padded(price), padded(quantity), total))
        index += 1
        sum += total
    file.write("----------------------------------------------------------------------\n")
    file.write("The total money to pay is: {0}".format(sum))
    file.close()

def store_receipt(data_dict):
    file = open("store_receipt.txt","at")
    sum = 0
    #index = 1
    for key in data_dict: 
        ID = key[0]  
        name = key[1]
        price = data_dict[key][0]
        quantity = data_dict[key][1]
        #total = price * quantity
        file.write("{0} {1} {2} {3}\n\n".format(ID, name, price, quantity))
        #index += 1
        #sum += total
    #file.write("{0}\n".format(sum))
    file.close()

def sale_report():
    file = open("store_receipt.txt")
    report_dict = {}
    for line in file:
        if line.strip():
            line = line.strip("\n").split(" ")
            key = (line[0],line[1])
            if key not in report_dict.keys():
                value = [int(line[2]),int(line[3])]
                report_dict[key] = value
            else:
                old_quantity = report_dict[key][1]
                new_quantity = int(line[3])
                report_dict[key][1] = old_quantity + new_quantity
    #print(report_dict)
    file.close()

    file = open("sale report.txt","at")
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

    file = open("sale report.txt")
    print(file.read())
    #return report_dict

def low_stock(data_dict):
    new_dict = {}
    for key in data_dict:
        quantity = int(data_dict[key][1])
        if quantity <= 5:
            new_dict[key] = data_dict[key]
    if new_dict != {}:
        print("Here is the list of low stock item")
        listing(new_dict)
    else:
        print("There is no low stock items.")

#def sale_report(data_dict):


def close_inventory(file_name, data_dict):
    file = open(file_name,"wt")
    for key in data_dict:
        ID = key[0]
        Name = key[1]
        Price = str(data_dict[key][0])
        Quantity = str(data_dict[key][1])
        file.write(ID + " " + Name + " " + Price + " " + Quantity + "\n")
    file.close()

def main():
    user_interface()
    data_dict = open_inventory()
    choice = 0.1
    while choice > 0 and choice <= 11:
        choice = int(input("What is your choice? "))
        if choice == 1:
            listing(data_dict)
        elif choice == 2:
            adding(data_dict)
        elif choice == 3:
            update_price(data_dict)
        elif choice == 4:
            remove(data_dict)
        elif choice == 5:
            sell(data_dict)
        elif choice == 6:
            restock(data_dict)
        elif choice == 7:
            search(data_dict)
        elif choice == 8:
            sale_report()
        elif choice == 9:
            low_stock(data_dict)
        elif choice == 11:
            break
        elif choice == 10:
            user_interface()
        else: 
            user_interface()
            choice = 0.1
            continue
        print()
        #user_interface()
    print("Thank you for visiting !!!")
    close_inventory("warehouse.txt", data_dict)
main()
