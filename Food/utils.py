import string
import random

from .models import Order

def random_id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))

    try:
        order = Order.objects.get(order_id=the_id)
        random_id_generator()

    except Order.DoesNotExist:
        return the_id


def transaction_id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))

    try:
        order = Order.objects.get(transaction_id=the_id)
        random_id_generator()

    except Order.DoesNotExist:
        return the_id
