from django.db import models
from django.utils.timezone import now
# Create your models here.

# accounts.models.py

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


"""
If you try to run an app with the code as it is now on your localhost, it will ostensibly work but you won’t be able to 
access the admin or add a user. The reason? You need to explicitly define this functionality via a user manager, and 
that’s where our CustomUserManager class comes in.You’ll need to define methods for create_user , create_superuser , and
get_by_natural_key at a minimum, or you will encounter errors. If you want to create more specific permissions groups, 
this is where you should define those as well.

"""
# Let define our model manager
class UserManager(BaseUserManager): # sub class the BaseUser Manager to create a user instance of the User
    #  set password's default = None, otherwise it would not pass?
    # checker must be passing "password" as a keyword argument
    # password = None means the minimal requirement is that "password" must exist as a parameter, but a default value is not required.
    # None is the default value for password if password is not explicitly provided.
    def create_user(self, email, password=None,is_active=True,is_staff=False,is_admin=False): # here the required arguments is email
        """
        Creates and saves an anonymous  User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        # define a variable user and assign it as a model field attribute of model manager
        # if not the email being passed into this create user model then just create it and passed an email
        user = self.model(
            # here self is BaseUserManager.Normalize the email address by lowercasing the domain part of it.
            email=self.normalize_email(email),# we can use it over and over again cz its a nomalize email
        )

        user.set_password(password) # user.password = password
        # will be stored as staff = 0 because is_staff is set to False
        user.staff = is_staff # additional parameter pass within the user object which will stored to the db as mention in the function definition or boolean field
        user.admin= is_admin
        user.active = is_active # by default set to true that means active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True # this controls access to the admin site.
        user.save(using=self._db) # user.save() is saving the data from the form to the database
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True #  when True, the user has all available permissions
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True, # We need to add the unique=True parameter to whatever field we are using as the USERNAME_FIELD
    )
    active = models.BooleanField(default=True) # can login
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.
    timestapm = models.DateTimeField(default=now())

    USERNAME_FIELD = 'email'  # that's how Django is going to recognize this user. It replaces the built-in username field for whatever you designate. In this case, we said it was the email.
    REQUIRED_FIELDS = [] # Email & Password are required by default.- by createsuperuser

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self): # add a get_short_name method, as Django expects a short name to be available for each user. This can be whatever field you want.
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None): # built in model permission
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    objects = UserManager()

# accounts.models.py



# # hook in the New Manager to our Model
# class User(AbstractBaseUser): # from step 2
#     ...
#     objects = UserManager()