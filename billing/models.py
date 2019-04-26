from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


User = settings.AUTH_USER_MODEL


# Create your models here.
class BillingProfile(models.Model):
    user = models.ForeignKey(User,unique=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32,null=True,blank=True)
    last_name = models.CharField(max_length=32,null=True,blank=True)
    phone_number = models.CharField(max_length=32,null=True,blank=True)
    address = models.CharField(max_length=120,null=True,blank=True)
    active = models.BooleanField(default=True,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)


    def __str__(self):
        return str(self.user)

     # A guest could have more than 1 billing profile
    # a logged in user could have only 1 billing profile



# generate a profile for every new user who signs up to your site
def create_billing_profile(sender,instance,created,*args,**kwargs):
    if created: # created means if new object is created or instantiated
        # creates a BillingProfile whenever it finds that a new user has been created... and set his user id as the insance id
        BillingProfile.objects.get_or_create(user=instance) # whenever  a new user instance has just been saved to the database!


post_save.connect(create_billing_profile,sender=User) # post_save will  'receive' the signal and hook in our own code to be executed at that point in the process when database in saved