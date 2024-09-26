from django.shortcuts import render
from catalog.models import Product
from django.views.generic import TemplateView, DetailView, ListView



# Create your views here
class ProductsListView(ListView):
    model = Product


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"


class ProductDetailView(DetailView):
    model = Product


# Ниже вариант FBV
# def home (request):
#     return render(request, 'home.html')
#
# def contacts (request):
#     return render(request, 'contacts.html')
#
# #
# def prod_list(request):
#     prods = Product.objects.all()
#     context = {"prods": prods}
#     return render(request, 'prod_list.html', context)
#
# #
# def prod_one(request, pk):
#     prod = Product.objects.get(pk=pk)
#     context = {"prod": prod}
#     return render(request, 'product_detail.html', context)