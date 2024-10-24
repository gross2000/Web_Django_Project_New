from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, ContactsTemplateView
from django.urls import reverse_lazy
from django.urls import reverse
from django.conf import settings

from catalog.views import home
# from catalog.views import contacts
# from catalog.views import prod_list
# from catalog.views import prod_one



app_name = CatalogConfig.name

# вариант CBV
urlpatterns = [
    path('', home, name="home"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create", ProductCreateView.as_view(), name="product_create"),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]


# вариант FBV
# urlpatterns = [path('', home, name = 'home'),
#     path('contacts/', contacts, name = 'contacts'),
#     path('products/', prod_list, name = 'products'),
#     path('products/<int:pk>/', prod_one, name = 'one_prod')]
