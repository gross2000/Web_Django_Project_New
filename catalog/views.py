from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from catalog.forms import ProductForm, VersionForm, ModeratorProductForm
from catalog.models import Product, Version
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied


# Create views here
def home(request):
    return render(request, 'catalog/home.html')  # Вариант FBV


class UserLoginRequiredMixin(LoginRequiredMixin):
    login_url = "/users/"
    permission_denied_message = "Только для авторизованных пользователей"


@login_required
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Имя пользователя : {name}\nТелефон: {phone}\nСообщение: {message}")
    return render(request, 'catalog/contacts.html')


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = "catalog.delete_product"
    success_url = reverse_lazy("catalog:product_list")


class ProductListView(ListView):
    model = Product
    permission_required = "catalog.view_product"
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    ordering = ["price"]  # сортирует товары по цене в порядке возрастания
    paginate_by = 10  # на странице показывает товары по 10 штук

    def get_context_data(self, *args, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        for product in context_data['object_list']:
            active_version = Version.objects.filter(product=product, is_active=True).first()
            product.active_version = active_version
        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(status=True)
        return queryset


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products : product_list')

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

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

    def get_form_class(self):
        user = self.request.user
        if self.object.user == user:
            return ProductForm
        if user.has_perm("catalog.can_change_status") and user.has_perm(
                "catalog.can_edit_description") and user.has_perm(
            "catalog.can_edit_category"):
            return ModeratorProductForm
        raise PermissionDenied


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.user = user
        product.save()
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductDetailView(DetailView):
    model = Product


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

class ModeratorProductUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ModeratorProductForm
    template_name = 'catalog/moderator_product_form.html'
    success_url = reverse_lazy('catalog:menu')
    permission_required = (
        'catalog.can_change_status',
        'catalog.can_edit_description',
        'catalog.can_edit_category',
    )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj

###################################################################################################
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
