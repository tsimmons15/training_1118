import mysql.connector

shopping_cart = mysql.connector.connect(user='root', database='shopping_cart')

def updateStock():
    