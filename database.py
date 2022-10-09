import sqlite3


class DatabaseActions:

    def __init__(self):
        self.connection = sqlite3.connect('tabris.db')
        self.cursor = self.connection.cursor()

    def find_by_name_db(self, name) -> list:
        """
        function takes product name from controller function and make sql request which search positions with similar name,
        then returns list object with results
        :param name:
        :return:
        """
        command = f'SELECT * FROM product WHERE name LIKE "%{name}%"'
        self.cursor.execute(command)
        result = self.cursor.fetchall()
        return result

    def find_by_sale_value_db(self, value1, value2) -> list:
        """
        function takes sale values from controller function and make sql request which search positions with sale
        between value1 and value2, then returns list object with results
        :param value1:
        :param value2:
        :return:
        """
        command = 'SELECT * FROM product WHERE sale >= ? and sale <= ?'
        self.cursor.execute(command, (value1, value2))
        result = self.cursor.fetchall()
        return result

    def add_card_db(self, name: str, sale, old_price, new_price, url):
        '''
        function takes few params  with product information from parcer function, then makes sql request
        which adds product card in database 'product' table
        :param name:
        :param sale:
        :param old_price:
        :param new_price:
        :param url:
        :return:
        '''
        command = f'INSERT INTO product VALUES(?, ?, ?, ?, ?)'
        self.cursor.execute(command, (name.lower(), sale, old_price, new_price, url))

    def database_commit(self):
        """
        function that commits database changes
        :return:
        """
        self.connection.commit()

    def clear_database(self):
        """
        function that clears table 'product' in database
        :return:
        """
        command = 'DELETE FROM product'
        self.cursor.execute(command)
        self.connection.commit()
        return True
