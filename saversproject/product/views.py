from django.shortcuts import get_object_or_404, render, redirect
from .models import *


# Create your views here.
def product(request):
    products = Product.objects.all()
    properties = ProductProperty.objects.all()
    propertynames = PropertyName.objects.all()    

    return render(request, 'product/product.html', {'products':products, 'properties':properties, 'propertynames':propertynames })

    
def detail(request, pk):
    product = Product.objects.get(pk=pk)
    properties = ProductProperty.objects.filter(product_id=pk)
    propertynames = PropertyName.objects.all()
    
    # current_user_pk = request.user.id
    return render(request, 'product/detail.html',{'product':product, 'properties':properties})

