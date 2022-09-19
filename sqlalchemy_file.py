import sqlite3

connection = sqlite3.connect('users.db')
cursor = connection.cursor()

sql = 'CREATE TABLE `sale_item`(name VARCHAR(255), url VARCHAR(255), sale FLOAT, old_price FLOAT, new_price FLOAT)'
cursor.execute(sql)
connection.commit()
cursor.execute('SELECT * FROM `sale_item` WHERE "sale" > 70')
product_list = cursor.fetchall()
for product in product_list:
    print(product)
