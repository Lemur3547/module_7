import stripe

stripe.api_key = "sk_test_51PqymIP32io8mk7XYu5ztjQj0484NL65d4xy6Cir7ZJJUSqloNhgUASzAMwHeq4gmiPNjXEum3gr63CEivirDOHq00sdKgOm9S"


def create_product(product):
    """Создает продукт"""
    return stripe.Product.create(name=f"{product}")


def create_price(price, product):
    """Создает цену в stripe."""
    return stripe.Price.create(
        currency="rub",
        unit_amount=price * 100,
        product=product.get('id')
    )


def create_session(price):
    """Создает сессию для оплаты"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url'), session.get('payment_method_types')[0]


def get_payment_status(payment_id):
    response = stripe.checkout.Session.retrieve(
        payment_id
    )
    return response.get('payment_status'), response.get('status')
