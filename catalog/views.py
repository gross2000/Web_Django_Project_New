from django.shortcuts import render
from catalog.models import Product

# Create your views here
def home (request):
    return render(request, 'home.html')

def contacts (request):
    return render(request, 'contacts.html')

# задание №2
def prod_list(request):
    prods = Product.objects.all()
    context = {"prods": prods}
    return render(request, 'prod_list.html', context)

# задание №1
def prod_one(request, pk):
    prod = Product.objects.get(pk=pk)
    context = {"prod": prod}
    return render(request, 'one_prod.html', context)