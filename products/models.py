from django.db import models
import os
import random
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import  slugify
from django.db.models.signals import pre_save # right before the model save we gonna do something
from django.contrib.auth import get_user_model as user_model



def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name,ext = os.path.splitext(base_name)
    return name,ext

def upload_image_path(instance,filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1,3910209312)
    name,ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return 'products/{new_filename}/{final_filename}'.format(
        new_filename=new_filename,final_filename=final_filename
    )


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    User = user_model()

    # creator = models.ForeignKey(User,on_delete=models.CASCADE)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_by_category', args=[self.name])







class ProductQuerySet(models.QuerySet): # we can use Queryset API
    def featured(self):
        return self.filter(featured=True)# filter()- queryset-api- Returns a new QuerySet containing objects that match the given lookup parameters.

    def available(self):
        return self.filter(available=True)

    def get_by_id(self,slug):
        qs =  self.filter(slug=slug) #return  Product.object or single product
        if qs.count()==1: #Returns an integer representing the number of objects in the database matching the QuerySet.
            return qs.first() # Returns the first object matched by the queryset, or None if there is no matching object.
            # If the QuerySet has no ordering defined, then the queryset is automatically ordered by the primary key.
        return None

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=30)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    short_descriptiton = models.TextField()
    full_descriptiton = models.TextField()
    specification = models.TextField()
    quantity = models.PositiveIntegerField(blank=True,default=15)
    price = models.DecimalField(decimal_places=2,default=39.99,max_digits=20)
    image = models.ImageField(null=True,blank=True,upload_to=upload_image_path)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)


    # objects = ProductManager()
    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.title # will return a string representation rather than product object

    def get_absolute_url(self): # to provide a link to a particular object or want to display that object's specific URL (if it has one) to the user
        return reverse("productdetail", kwargs={'slug': self.slug})
        #return '/products/{slug}'.format(slug=self.slug)

from .utils import unique_slug_generator

 # lets define a receiver signal function for creating slug which will takes a sender argument-in this case Produc Model, along with wildcard keyword arguments (**kwargs--slug); all signal handlers must take these arguments.
# The callback function which will be connected to the pre_save signal receiver
def pre_save_post_receiver(sender,instance, *args,**kwargs):  # here keyword instance arguments refer to the model itself to make sure this function send every time when we create title or slug we need a sender signal to do so
    if not instance.slug:  # if there is no slug present
        # instance.slug = create_slug(instance)
        instance.slug = unique_slug_generator(instance) # if slug field is not exist in the model ..generate it

# pre_save will sent at the beginning of a model’s save() method.
# here sender is the model class
# connect the  receiver to the signal
pre_save.connect(pre_save_post_receiver,sender=Product) # the sender will be the model class being saved, so you can indicate that you only want signals sent by some model:
# signal pre_save will run the function before every time a model is created or gets save
