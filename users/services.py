import os
from dotenv import load_dotenv
import stripe
from config.settings import BASE_DIR

load_dotenv(BASE_DIR / '.env', override=True)
stripe.api_key = os.getenv('stripe_api_key')


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
