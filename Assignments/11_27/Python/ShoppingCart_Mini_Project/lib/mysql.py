import mysql.connector


def getConnection():
    return mysql.connector.connect(user='root', database='shopping_cart')


insertStockQuery = "insert into products (product_name, quantity, price) values (%s, %s, %s)"
updateStockQuantityQuery = "update products set quantity = %s where serial_number = %s"
updateStockQuantityQuery = "update products set price = %s where serial_number = %s"
deleteStockQuery = "delete from products where serial_number = %s"
insertCartQuery = "insert into order_item (order_num, serial_number) values (%s, %s)"
updateCartQuery = "update order_item set quantity = %s"
deleteCartQuery = "delete from order_item where order_item_id = %s"
insertCustomer = "insert into customer (name, address, distance) values (%s, %s, %s)"
updateReference = "update reference set reference_value = %s where reference_name = %s"


def insertStock(itemToInsert):
    dbh = getConnection()
    cursor = dbh.cursor()
    cursor.execute(insertStockQuery, itemToInsert)
    product_id = cursor.lastrowid
    db_handler.commit()
    cursor.close()
    dbh.close()


def updateStock(itemToUpdate):
    dbh = getConnection()
    cursor = dbh.cursor()

    # Error handling
    # ...
    db_handler.commit()
    cursor.close()
    dbh.close()



def deleteStock(itemToDelete):
    dbh = getConnection()
    cursor = dbh.cursor()

    # Error handling
    # ...
    db_handler.commit()
    cursor.close()
    dbh.close()

def insertCart(itemToInsert):
    dbh = getConnection()
    cursor = dbh.cursor()

    # Error handling
    # ...
    db_handler.commit()
    cursor.close()
    dbh.close()

def updateCart(itemToUpdate):
    dbh = getConnection()
    cursor = dbh.cursor()

    # Error handling
    # ...
    db_handler.commit()
    cursor.close()
    dbh.close()

def deleteCart(itemToDelete):
    dbh = getConnection()
    cursor = dbh.cursor()

    # Error handling
    # ...
    db_handler.commit()
    cursor.close()
    dbh.close()

def insertCustomer(customerToInsert):
    dbh = getConnection()
    cursor = dbh.cursor()

    # Error handling
    # ...
    db_handler.commit()
    cursor.close()
    dbh.close()

def updateReference(referenceName, updateValue):
    dbh = getConnection()
    cursor = dbh.cursor()

    # Error handling
    # ...
    db_handler.commit()
    cursor.close()
    dbh.close()
