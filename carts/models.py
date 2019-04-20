from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save,m2m_changed
User = settings.AUTH_USER_MODEL

class CartManager(models.Manager): # handle the business logic of cart
    def get_cart_or_create(self,request): # get existing cart-means stored in cache by user in past or create a new one
        # define a variable cart_id which will check the session if there is any item exist in the cart or not
        cart_id = request.session.get('cart_id', None)  # if there is cart get the cart id or if not any cart exist set it to NOne
        qs = self.get_queryset().filter(id=cart_id) # just filter the cart_id with get_queryset, qs will check the data searchng by and id , if there is any card_id available
        if qs.count() == 1:  # select the number of rows matching the query and check there is one
            new_obj = False # we set it False initially  because the object is not new,and its the existed one which is a previous cart,
            print('card id exist- cause its stored in session')
            cart_obj = qs.first()  # if there is one item we retrieve it by first() and store it by variable cart_obj
            if request.user.is_authenticated and cart_obj.user is None: # if user is an authenticated user and not saved earliar with corrosponding cart id that means the cart_user_id table row is empty
                cart_obj.user = request.user # referring  the current logged in users as the user of the cart
                cart_obj.save() # save the cart
        else: # if there is not any existing cart in the session
            print("New cart created")
            # now create a object cart_obj of the Cart model which will instantiate the Cart- will need user as as argument
            cart_obj = Cart.objects.create_cart(user=request.user)  # creating another cart because it doesn't exist
            new_obj = True # because its new cart
            request.session['cart_id'] = cart_obj.id # the corresponding cart id will be passed in the session and stored in the variable cart_id
        return cart_obj,new_obj # passing the two object either new cart or existing cart


    def create_cart(self,user=None):
        user_obj = None # primarily empty or initialize the user_obj as NOne  - there is no user
        if user is not None:
            if user.is_authenticated: # check if user is valid user
                user_obj = user_obj # change the user None to existed one- because there is one authenticate user
        # To create and save an object in a single step, use the create() method.
        return self.model.objects.create(user=user_obj) # instantiate the user attribute of the Cart model class with the create method and the variable user_obj

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) # any user both logged in and anonymous can add to cart
    products = models.ManyToManyField(Product,blank=True) # cart can be empty
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Django adds a Manager with the name "objects" to every Django model class.
    objects = CartManager() # pass all the business logic of CartManager to the Cart Model class- similar to inheritance
    # NOw we can access all the method and attribute of CartManager class

    def __str__(self):
        return str(self.id)




def m2m_changed_cart_receiver(sender,instance,action,*args,**kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all() # here instance keyword refer to the Current Instance we are working with
        total = 0
        subtotal = 0
        for item in products:
            total+= item.price
        print(total)
        print(subtotal)
        instance.subtotal =  total
        instance.save()

m2m_changed.connect(m2m_changed_cart_receiver,sender=Cart.products.through)

def pre_save_cart_receiver(sender,instance,*args,**kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal +10  #*1.08
    else:
        instance.total = 0.00

pre_save.connect(pre_save_cart_receiver,sender=Cart)