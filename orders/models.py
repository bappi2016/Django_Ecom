import math
from django.db import models
from django.db.models.signals import pre_save,post_save
from carts.models import Cart
from .utils import unique_order_id_generator
# Create your models here.





ORDER_STATUS_CHOICES = (
    ('created','Created'), # Capitalize option will show in the interface
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),
)

class Order(models.Model):
    # at first we need at order id attribute - which will represents all the distinct orders
    order_id = models.CharField(max_length=120,null=True,blank=True) # ABCD1478DD
    # billing profile = ?
    # shipping profile
    # billing address
    # cart - in order to add cart we have to connect the cart model to this order model
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE) # here we connect the Cart model with Order model
    status = models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES) # status refer to either the cart is submit or not
    shipping_total = models.DecimalField(default=5.99,max_digits=100,decimal_places=2)
    total = models.DecimalField(default=0.00,max_digits=100,decimal_places=2)


    def __str__(self):
        return  self.order_id


    def update_total(self): # on the order self
        cart_total = self.cart.total # grab the current total of cart(attribute of Cart) and store it as cart_total
        shipping_total = self.shipping_total
        new_total =  math.fsum([cart_total,shipping_total])
        self.total = new_total
        self.save()
        return new_total

# generate the order id

def order_id_genarator(sender,instance,*args,**kwargs):
    if not instance.order_id: # if there is not any order_id of the model instance
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(order_id_genarator,sender=Order)


# post_save_cart_total
def calculate_cart_total(sender,instance,created,*args,**kwargs):
    # if not created - created = False - to ensure that or assume our signal will trigger only once if the corresponding instance doesn't exist yet- then create the instance
    if not created: # let assume the cart is not created yet  or didn't exist- means there is no order yet- we will calculate this
        # first make the instance or refer the instance of cart_obj
        cart_obj = instance
        cart_total = cart_obj.total # grab the current cart total
        cart_id = cart_obj.id # grab the cart id
        # now run a query to fetch if there is any cart exist with the lookup cart_id
        qs = Order.objects.filter(cart__id=cart_id) # here 'cart _ _ id 'is the cart attribute of the Order and id is the lookup , cart_id is what we are looking for or the data
        if qs.count() == 1 : # if qs exist we will update the cart with total
            order_obj = qs.first() # set the first match queryset as a order obj
            order_obj.update_total() # ok, by this the cart is now created with the updated  total- now the order is exists - lets update the order now

# Now pass the cart_total in the model after the model saved with post save

post_save.connect(calculate_cart_total,sender=Cart) # Now the cart is changes with the updated total


# Now the cart is changes with the updated cart or product - what about the order now- we have to update it too

# we can do the same logic - means pass a signal  after the order saved
# post save order_update- the receiver function
def order_update(sender,instance,created,*args,**kwargs):
    # created - the signal will trigger if the instance is exist - created = True
    print('running')
    if created: # if cart is created and updated. update the order total in the order model
        print('Updating...')
        instance.update_total() # take the class method as instance attribute and update it when the update is change

post_save.connect(order_update,sender=Order) # dispatch the signal



# """
# GENDER_CHOICES = (
# ('M', 'Male'),
# ('F', 'Female'),
# ('P', 'Prefer not to answer'),
# )
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, related_name='profile')
#     nickname = models.TextField(max_length=64, null=True, blank=True)
#     dob = models.DateField(null=True, blank=True)
#     gender = models.CharField(max_length=1,
#                               choices=GENDER_CHOICES, default='M')
#     bio = models.TextField(max_length=1024, null=True, blank=True)
#     [...]
#
#
#
# def save(self, *args, *kwargs):
#     u = super(User, self).save(*args, **kwargs)
#     UserProfile.objects.get_or_create(user_id=u.id)
#     return u # save needs to return a `User` object, remember!
#
#
# @receiver(post_save, sender=User)
# def ensure_profile_exists(sender, **kwargs):
#     if kwargs.get('created', False):
#         UserProfile.objects.get_or_create(user=kwargs.get('instance'))
#
# The kwargs variable is an example of the post_save signal being extra-efficient -
# it sends out highly-relevant information pertaining to the Signal-sender.
# Typically, the post_save signal sends out a copy of the saved instance and a boolean
# variable called created that indicates whether a new instance was created or an older
# instance was saved/updated. There are a few other things that are bundled into the kwargs
# dictionary but it is these two variables that we shall use to carry out our ultimate task -
# that of creating a UserProfile whenever a new User is created.
#
# therefore, simply checks for the (boolean-)value of the created
# key in the kwargs dictionary (assuming it to be False, by default) and creates a UserProfile
# whenever it finds that a new user has been created...
#
#
#
# """