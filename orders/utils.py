import random
import string
from django.utils.text import slugify



def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def unique_order_id_generator(instance): # instance refer to the model instance
    new_order_id = random_string_generator()

    Klass = instance.__class__
    # here order_id is the model field attribute
    qs_exists = Klass.objects.filter(order_id=new_order_id).exists() # if the slug is present or not
    if qs_exists: # if an order id is  already exists create a new order_id with random string

        return unique_order_id_generator(instance)
    return new_order_id



