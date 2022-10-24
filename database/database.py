import psycopg2
from config import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT

class DataBase:
    def __init__(self):
        self.database = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    '''MANAGER ORQALI SQL SAVOLLARNI ISHLATING!'''
    def manager(self, sql, *args,
                fetchone:bool=False,
                fetchall:bool=False,
                fetchmany:bool=False,
                commit:bool=False):
        with self.database as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    result = db.commit()
                elif fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()
                elif fetchmany:
                    result = cursor.fetchmany()
            return result

    def create_users_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            user_full_name VARCHAR(30),
            phone_number VARCHAR(18),
            birth_date DATE
        )'''
        self.manager(sql, commit=True)

    def insert_telegram_id(self, telegram_id):
        sql = '''INSERT INTO users(telegram_id)
        VALUES (%s)
        ON CONFLICT DO NOTHING'''
        self.manager(sql, (telegram_id,), commit=True)

    def check_user_for_registration(self, telegram_id):
        sql = '''SELECT user_full_name, phone_number, birth_date FROM users
        WHERE telegram_id = %s'''
        return self.manager(sql, telegram_id, fetchone=True)

    def save_user(self, name, phone, b_data, telegram_id):
        sql = '''UPDATE users SET user_full_name = %s, phone_number = %s, birth_date = %s
        WHERE telegram_id = %s'''
        self.manager(sql, name, phone, b_data, telegram_id, commit=True)

    def create_table_categories(self):
        sql = '''CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            category_name VARCHAR(30) UNIQUE
        )'''
        self.manager(sql, commit=True)

    def create_table_products(self):
        sql = '''CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            product_name VARCHAR(200) UNIQUE,
            product_link TEXT,
            product_price INTEGER,
            product_image TEXT,
            category_id INTEGER REFERENCES categories(category_id)
        )'''
        self.manager(sql, commit=True)

    def insert_categories(self, category_name):
        sql = '''INSERT INTO categories(category_name)
        VALUES (%s)
        ON CONFLICT DO NOTHING'''
        self.manager(sql, (category_name,), commit=True)

    def insert_products(self, product_name, product_link, product_price, product_image, category_id):
        sql = '''INSERT INTO products (product_name, product_link, product_price, product_image, category_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING'''
        self.manager(sql, product_name, product_link, product_price, product_image, category_id, commit=True)

    def select_category_by_cat_name(self, category_name):
        sql = '''SELECT category_id FROM categories
        WHERE category_name = %s'''
        return self.manager(sql, category_name, fetchone=True)

    def select_all_categories(self):
        sql = '''SELECT category_name FROM categories'''
        return self.manager(sql, fetchall=True)

    def select_products_by_category_id(self, category_id):
        sql = '''SELECT product_name, product_id FROM products WHERE category_id = %s'''
        return self.manager(sql, category_id, fetchall=True)

    def select_products_by_pagination(self, category_id, offset, limit):
        sql = '''SELECT product_name, product_id FROM products WHERE category_id = %s
        OFFSET %s
        LIMIT %s'''
        return self.manager(sql, category_id, offset, limit, fetchall=True)

    def count_products_by_category_id(self, category_id):
        sql = '''SELECT count(product_id) FROM products WHERE category_id = %s'''
        return self.manager(sql, category_id, fetchone=True)[0]

    def get_product_by_id(self, product_id):
        sql = '''SELECT product_name, product_link, product_price, product_image, category_id
        FROM products WHERE product_id = %s'''
        return self.manager(sql, product_id, fetchone=True)

    def create_table_order(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            customer_name TEXT NOT NULL,
            date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )'''
        self.manager(sql, commit=True)

    def create_table_order_item(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS orderitem(
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            product_name TEXT,
            product_quantity INTEGER,
            product_price BIGINT,
            product_total_price BIGINT,
            order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE
        )'''
        self.manager(sql, commit=True)

    def insert_order(self, customer_name):
        sql = '''
        INSERT INTO orders(customer_name)
        VALUES (%s) returning *'''
        return self.manager(sql, (customer_name,), fetchone=True)

    def insert_order_item(self, product_name, product_quantity, product_price, product_total_price, order_id):
        sql = '''
        INSERT INTO orderitem(product_name, product_quantity, product_price, product_total_price, order_id)
        VALUES (%s, %s, %s, %s, %s)'''
        self.manager(sql, product_name, product_quantity, product_price, product_total_price, order_id, commit=True)

