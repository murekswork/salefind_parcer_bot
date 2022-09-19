import sqlite3

connection = sqlite3.connect('users.db')
cursor = connection.cursor()

def delete_db():
    sql = 'DELETE FROM `sale_item`'
    cursor.execute(sql)
    connection.commit()
    print('Запрос на очистку БД выполнен!')

def add_product(name, url, sale, old_price, new_price):
    sql = f'INSERT INTO `sale_item`(`name`, `url`, `sale`, `old_price`, `new_price`) VALUES("{name}", "{url}", "{sale}", "{old_price}", "{new_price}")'
    cursor.execute(sql)
    print('Товар добавлен')

def search_by_name(product_name):
    sql = f'SELECT * FROM `sale_item` WHERE `name` LIKE "%{product_name}%"'
    cursor.execute(sql)
    response = cursor.fetchall()
    message = []
    if len(response) != 0:
        for i in response:
            message.append([i[0], i[1], i[2], i[3], i[4]])
        with open(f'{product_name}.txt', encoding='utf8', mode='a') as f:
            for item in response:
                f.write(f'Товар: {item[0]}\n'
                        f'Ссылка: {item[1]}\n'
                        f'Скидка: {item[2]}%\n'
                        f'Старая цена: {item[3]}\n'
                        f'Новая цена: {item[4]}\n\n')
        print('Запрос поиска по названию выполнен!')
        return message
    else:
        return False


def bot_sales_find(n, m):
    sql = f'SELECT * FROM `sale_item` WHERE `sale` > {n} and `sale` <= {m}'
    cursor.execute(sql)
    response = cursor.fetchall()
    message = []
    for i in response:
        message.append([i[0], i[1], i[2], i[3], i[4]])
    with open(f'от_{n}_до_{m}_скидки.txt', encoding='utf8', mode='a') as f:
        for item in response:
            f.write(f'Товар: {item[0]}\n'
                    f'Ссылка: {item[1]}\n'
                    f'Скидка: {item[2]}%\n'
                    f'Старая цена: {item[3]}\n'
                    f'Новая цена: {item[4]}\n\n')
    print('Запрос по выдаче скидки успешно обработан')
    return message


def commit():
    connection.commit()