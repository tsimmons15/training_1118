from util.logging import setup_logger



logger = setup_logger(name="shoppingCart", enableConsole=False)

stock = {
    1: {"name": "Biscuits", "quantity": 5, "price": 20.50},
    2: {"name": "Cereals", "quantity": 3, "price": 90.00},
    3: {"name": "Chicken", "quantity": 5, "price": 100.00}
}

customerDetails = {
}

cart = {
}

deliveryThresholds = [15, 30]
deliveryCharges = [50, 100]

adminCreds = "admin"

def main():
    # Read from db
    # TODO
    inputContinue = True

    while inputContinue:
        showMenu()

        userInput = int(input())
        logger.info(f"User entered: {userInput}")
        match userInput:
            case 1:
                logger.info("Editing cart.")
                editCart()
            case 2:
                logger.info("Checking out.")
                checkout()
            case 3:
                logger.info("Admin log in.")
                adminLogin()
            case 4:
                print("Good bye!")
                logger.info("User logged out")
                inputContinue = False
            case _:
                print("Unrecognized input")
                logger.warn("Unrecognized input from user.")

def showMenu():
    print("1) Edit Cart")
    print("2) Check out")
    print("3) Admin")
    print("4) Exit")

def showCartMenu():
    print("1) Show stock")
    print("2) Show cart")
    print("3) Edit item")
    print("4) Add item")
    print("5) Exit")

def editCart():
    inputContinue = True

    while inputContinue:
        showCartMenu()

        userInput = int(input())

        match (userInput):
            case 1:
                logger.info("Stock being displayed")
                displayStock()
            case 2:
                logger.info("Cart being displayed")
                if len(cart) == 0:
                    print("No items!")
                else:
                    displayCart()
            case 3:
                logger.info("Changing cart quantity")
                if len(cart) == 0:
                    print("No items!")
                else:
                    editItem()
            case 4:
                logger.info("Adding to cart...")
                addItem()
            case 5:
                print("Good bye!")
                logger.info("User logged out")
                inputContinue = False
            case _:
                print("Unrecognized input...")
                logger.warn("Unrecognized input from user.")

def displayStock():
    #Update stock.
    #TODO
    for serial,item in stock.items():
        printStockItem(item)

def printStockItem(item):
    print(f"{item['name']} (${item['price']}). Remaining {item['quantity']}.")

def displayCart():
    for item in cart:
        printCartItem(item)

def printCartItem(item):
    print(f"{stock[item]['name']:10} ({cart[item]:10}). Subtotal: ${cart[item] * stock[item]['price']:10}")

def editItem():
    displayCart()
    attempts = 0
    inputContinue = True

    while inputContinue:
        print("Enter the item to modify: ")
        userInput = int(input())

        if (attempts < 4 and userInput in stock and userInput in cart):
            item = userInput
            print("Enter amount to add: ")
            userInput = int(input())
            print("User input: ", userInput, "cart[item]: ", cart[item])
            if ((userInput >= 0 and userInput < stock[item]["quantity"]) or

                (userInput >= 0 or (userInput*-1) < cart[item])):
                cart[item] += userInput
                if cart[item] == 0:
                    del cart[item]
                stock[item]["quantity"] -= userInput
                logger.info(f"User added {userInput} of {stock[item]['name']} to cart.")
                # Save to DB
                #TODO
                inputContinue = False
            else:
                print("Invalid amount. Please enter a valid amount.")
                logger.warn(f"User tried to add invalid amount to cart. Amount: {userInput}.")
        elif (attempts < 4 and userInput not in cart):
            print(f"{userInput} is not in the cart to modify. Please add it")
            logger.warn(f"User tried to edit item {userInput} that is not in cart. {3 - attempts} attempts remaining.")
            attempts += 1
        elif (attempts < 4):
            attempts += 1
            print(f"Invalid stock number. {3 - attempts} attempts remaining.")
            logger.warn("User tried to edit an invalid item in their cart.")
        else:
            inputContinue = False
            logger.warn("Too many attempts to enter stock number.")
            print("Invalid stock number. Too many attempts, returning.")

def addItem():
    displayStock()
    attempts = 0
    inputContinue = True

    while inputContinue:
        print("Enter the item to add: ")
        userInput = int(input())

        if (attempts < 4 and userInput in stock):
            item = userInput
            print("Enter amount to add: ")
            userInput = int(input())
            if item in cart:
                print("Item already added, please modify instead.")
                logger.warn("User tried to add item already in cart.")
            elif (userInput >= 0 and userInput < stock[item]["quantity"]):
                cart[item] = userInput
                stock[item]["quantity"] -= userInput
                print(stock[item])
                logger.info(f"User added {userInput} of {stock[item]['name']} to cart.")
                # Save to DB
                #TODO
                inputContinue = False
            else:
                print("Invalid amount. Please enter a valid amount.")
                logger.warn(f"User tried to add invalid amount to cart. Amount: {userInput}.")
        elif (attempts < 4):
            attempts += 1
            print(f"Invalid stock number. {3 - attempts} attempts remaining.")
            logger.warn("User attempted to add invalid stock number to cart.")
        else:
            inputContinue = False
            logger.warn("Too many attempts to enter stock number.")
            print("Invalid stock number. Too many attempts, returning.")

def checkout():
    print("Please enter your name: ")
    customerDetails["name"] = input()

    print("Please enter your address: ")
    customerDetails["address"] = input()

    inputContinue = True

    while inputContinue:
        print("Please enter the distance to ship: ")
        distance = int(input())

        if distance <= 0 or distance > deliveryThresholds[1]:
            print("We either do not ship that far, or you've entered a negative or 0 value. Please reenter: ")
            logger.warn(f"Invalid shipping distance provided. Distance: {distance}")
        else:
            customerDetails["deliveryCharge"] = calculateDeliveryCharge(distance)
            inputContinue = False

    displayBill()
    print(f"Name: {customerDetails['name']}")
    print(f"Address: {customerDetails['address']}")

    print("Thank you for ordering. Please order again.")

def calculateDeliveryCharge(distance):
    result = 0
    if distance < deliveryThresholds[0]:
        result = deliveryCharges[0]
    else:
        result = deliveryCharges[1]
    
    return result

def displayBill():
    price = 0
    print("------------------------------Bill------------------------------")
    print(f"  {'S.No':10}   {'Item':10}   {'Qty':10}   {'Total Cost':10}")
    for item in cart:
        price += cart[item] * stock[item]["price"]
        print(f"  {item:10}   {stock[item]['name']:10}   {cart[item]:10}   {cart[item] * stock[item]['price']:10}")
    print("----------------------------------------------------------------")
    print(f"{' Total Items Cost: ':39} ${price}")
    customerDetails["subtotal"] = price
    print(f"Delivery surcharge: ${customerDetails['deliveryCharge']}")
    customerDetails["total"] = customerDetails["deliveryCharge"] + price
    print(f"Total cost: ${customerDetails['total']}")
    

def adminLogin():
    attempts = 0
    login = False

    while attempts < 4:
        print("Please enter the admin password: ")
        userInput = input()
        #print("userInput: ", userInput, "adminCreds: ", adminCreds)
        if userInput == adminCreds:
            print("Welcome!")
            logger.info("Admin login used.")
            login = True
            break


        else:
            print(f"Invalid login. Please try again ({3 - attempts} attempts remaining)")
            attempts += 1
            logger.warn("Invalid login attempted.")
    
    if login:
        admin()

def admin():
    inputContinue = True
    attempts = 0

    while inputContinue:
        showAdminMenu()
        userInput = int(input())

        match userInput:
            case 1:
                displayStock()
                attempts = 0
                inputContinue = True

                while inputContinue:
                    print("Enter the item to modify: ")
                    userInput = int(input())

                    if (attempts < 4 and userInput in stock):
                        item = userInput
                        print("Enter amount to add: ")
                        userInput = int(input())

                        if (userInput >= 0):
                            stock[item]["quantity"] += userInput
                            # Save to DB
                            #TODO
                            inputContinue = False
                        else:
                            print("Invalid amount. Please enter a valid amount.")
                            logger.warn(f"Admin tried to order invalid amount. Amount: {userInput}.")
                    elif (attempts < 4):
                        attempts += 1
                        print(f"Invalid stock number. {3 - attempts} attempts remaining.")
                    else:
                        inputContinue = False
                        logger.warn("Too many attempts to enter stock number.")
                        print("Invalid stock number. Too many attempts, returning.")
                inputContinue = True
            case 2:
                displayStock()
                attempts = 0
                inputContinue = True

                while inputContinue:
                    print("Enter the item to modify: ")
                    userInput = int(input())

                    if (attempts < 4 and userInput in stock):
                        item = userInput
                        print("Enter amount to add: ")
                        userInput = int(input())

                        if (userInput >= 0):
                            stock[item]["price"] = userInput
                            # Save to DB
                            #TODO
                            inputContinue = False
                        else:
                            print("Invalid amount. Please enter a valid amount.")
                            logger.warn(f"Admin tried to change price to a negative value. Amount: {userInput}.")
                    elif (attempts < 4):
                        attempts += 1
                        print(f"Invalid stock number. {3 - attempts} attempts remaining.")
                    else:
                        inputContinue = False
                        logger.warn("Too many attempts to enter stock number.")
                        print("Invalid stock number. Too many attempts, returning.")
                inputContinue = True
            case 3:
                inputContinue = True
                while inputContinue:
                    print(f"Enter new lower threshold (currently: {deliveryThresholds[0]})")
                    userInput = int(input())
                    if userInput <= 0:
                        print("Invalid amount. Please enter a positive number.")
                        logger.warn(f"Admin entered a negative delivery threshold lower bound. Lower bound: {userInput}")
                    else:
                        deliveryThresholds[0] = userInput
                        logger.info(f"Delivery threshold lower bound has been changed to: {deliveryThresholds[0]}.")
                        print("Lower bound updated.")
                inputContinue = True
                while inputContinue:
                    print(f"Enter new upper threshold (currently: {deliveryThresholds[1]})")
                    userInput = int(input())
                    if userInput <= 0:
                        print("Invalid amount. Please enter a positive number.")
                        logger.warn(f"Admin entered a negative delivery threshold upper bound. Lower bound: {userInput}")
                    else:
                        deliveryThresholds[1] = userInput
                        logger.info(f"Delivery threshold upper bound has been changed to: {deliveryThresholds[0]}.")
                        print("Upper bound updated.")
                        inputContinue = False
                inputContinue = True
                while inputContinue:
                    print(f"Enter new short distance discount (currently: {deliveryCharges[0]})")
                    userInput = float(input())
                    if userInput <= 0:
                        print("Invalid amount. Please enter a positive number.")
                        logger.warn(f"Admin entered a negative short distance discount. Discount: {userInput}")
                    else:
                        deliveryCharges[0] = userInput
                        logger.info(f"Short distance discount has been changed to: {deliveryCharges[0]}.")
                        print("Short distance discount updated.")
                inputContinue = True
                while inputContinue:
                    print(f"Enter new long distance charge (currently: {deliveryCharges[1]})")
                    userInput = float(input())
                    if userInput <= 0:
                        print("Invalid amount. Please enter a positive number.")
                        logger.warn(f"Admin entered a negative long distance charge. Long distance charge: {userInput}")
                    else:
                        deliveryCharges[1] = userInput
                        logger.info(f"Long distance charge has been changed to: {deliveryCharges[1]}.")
                        print("Long distance charge.")
                        inputContinue = False
                inputContinue = True
            case 4:
                print("Good bye!")
                logger.info("User logged out")
                inputContinue = False
                break
            case _:
                print("Unrecognized input")
                logger.warn("Unrecognized input from user.")
        

def showAdminMenu():
    print("1) Order items.")
    print("2) Change price.")
    print("3) Change delivery charge.")
    print("4) Exit")