from django.shortcuts import render
from django.contrib.auth import authenticate,get_user_model
# Create your views here.
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import  reverse
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, FormView, RedirectView


from .forms import RegisterForm,UserRegistrationForm


User = get_user_model()
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'form.html'
    success_url = '/accounts/login'

class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/'
    form_class = AuthenticationForm
    template_name = 'login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)




class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/auth/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)