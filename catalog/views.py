from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory


# Create my views here
def home (request):
    return render(request, 'catalog/home.html') # Вариант FBV


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products : product_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data


    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))



class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        for product in context_data['object_list']:
            active_version = Version.objects.filter(product=product, is_active=True).first()
            product.active_version = active_version
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')


class ProductDetailView(DetailView):
    model = Product


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"


# Вариант FBV
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
#     return render(request, 'products_list.html', context)
#
# #
# def prod_one(request, pk):
#     prod = Product.objects.get(pk=pk)
#     context = {"prod": prod}
#     return render(request, 'product_detail.html', context)
