def get_welcome_message():
    return (
        "Добро пожаловать в бот MAGNIFINS! 🛍️"
    )

def get_cart_message(items, total_price):
    if not items:
        return "Ваша корзина пуста."

    cart_text = "Ваша корзина:\n"
    for index, item in enumerate(items):
        cart_text += f"{index + 1}. {item['name']}: {item['price']} руб.\n"
    cart_text += f"\nИтого: {total_price} руб."
    return cart_text

def get_product_added_message(product_name):
    return f"Товар {product_name} добавлен в корзину! 🛒"

def get_product_removed_message(product_name):
    return f"Товар {product_name} удален из корзины."

def get_order_placed_message():
    return (
        "Ваш заказ оформлен! 🎉\n\n"
        "Для уточнения деталей свяжитесь с нашим менеджером: @manager_username.\n"
        "Он поможет вам с оформлением и ответит на все вопросы."
    )

def get_admin_welcome_message():
    return "Добро пожаловать в админ-панель!"

def get_product_list_message(products):
    if not products:
        return "Нет доступных продуктов."

    products_text = "Список продуктов:\n"
    for product in products:
        products_text += f"{product['id']}. {product['name']} - {product['price']} руб.\n"
    return products_text

def get_product_added_admin_message(name, price):
    return f"Продукт {name} добавлен с ценой {price} руб."

def get_product_removed_admin_message(name):
    return f"Продукт {name} удален."

def get_product_edited_admin_message(name, price):
    return f"Продукт {name} обновлен с ценой {price} руб."