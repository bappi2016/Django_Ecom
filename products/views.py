from django.shortcuts import render,Http404
from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.views import View
from .models import Product
from django.views.generic import ListView,DetailView,\
    CreateView,UpdateView,DeleteView,FormView #Generic editing views for editing content

# Create your views here.

class ProductFeaturedListView(ListView):
    model = Product # The model that this view will display data for
    template_name = 'home.html'
    # context_object_name = 'product'  # Designates the name of the variable to use in the context.
    paginate_by = 3
    # queryset = Product.objects.featured().active()

    # def get_queryset(self):
    #     return Product.objects.all()

    # def get_context_data(self, *args,  **kwargs):
    #     context = super(ProductFeaturedListView,self).get_context_data(*args,**kwargs)
    #     return context



class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/featured_product_detail.html'
    def get_object(self,*args,**kwargs):

        request = self.request
        slug = self.kwargs.get(self.slug_url_kwarg)
        # instance = get_object_or_404(Post, slug=slug)
        instance = Product.objects.active().get_by_id(slug=slug)
        if instance is None:
            raise Http404('Product doesn\'t exist')
        return instance

class ProductListView(ListView):
    model = Product # The model that this view will display data for
    template_name = 'home.html'
    # context_object_name = 'product'  # Designates the name of the variable to use in the context.
    # paginate_by = 3
    queryset = Product.objects.all()

    def get_context_data(self, *args,  **kwargs): # Returns context data for displaying the object.
        context = super(ProductListView,self).get_context_data(*args,**kwargs)
        return context

class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/product_detail.html'

    def get_object(self,*args,**kwargs): # Returns the single object that this view will display.
        request = self.request
        slug = self.kwargs.get('slug')  # look kwargs slug in the urls  instead of default pk
        # instance = get_object_or_404(Product, slug=slug)
        instance = Product.objects.get_by_id(slug)
        if instance is None:
            raise Http404('Product doesn\'t exist')
        return instance

    def get_context_data(self, *args,**kwargs):
        context = super(ProductDetailView, self).get_context_data(*args,**kwargs)
        return context

