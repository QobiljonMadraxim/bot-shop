def create_tables(database, pars_oop):
    database.create_table_categories()
    database.create_table_products()

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