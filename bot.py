'''
BOTNI ISHGA TUSHIRISH
'''
from middlewares import SimpleMiddleware
from data.loader import bot, db
import handlers
from parser import OpenShopParser

db.create_users_table()


def create_tables(database, pars_oop):
    database.create_table_categories()
    database.create_table_products()
    database.create_users_table()

    database.insert_categories('phones')
    database.insert_categories('tv')
    database.insert_categories('air-conditioners')
    database.insert_categories('stiralniye-mashini')

    product_list = [pars_oop('phones').get_info(), pars_oop('tv').get_info(), pars_oop('air-conditioners').get_info(),
                    pars_oop('stiralniye-mashini').get_info()]

    for item in product_list:
        for product in item:
            cat_id = product['category_id']
            name = product['title']
            image = product['image']
            link = product['link']
            price = product['price']

            database.insert_products(name, link, price, image, cat_id)


bot.setup_middleware(SimpleMiddleware(0.5)) # bu botga qayta qayta yozmaslik uchun limit(sekundda) kiritiladi

if __name__ == '__main__':
    # bot.polling(none_stop=True)
    create_tables(db, OpenShopParser)
    bot.infinity_polling()
