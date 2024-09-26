from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductsListView, ContactsTemplateView, ProductDetailView
from django.conf import settings
# from catalog.views import home
# from catalog.views import contacts
# from catalog.views import prod_list
# from catalog.views import prod_one



app_name = CatalogConfig.name

# вариант CBV
urlpatterns = [
    path("", ProductsListView.as_view(), name="home"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("products/", ProductsListView.as_view(), name="prod_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]


# вариант FBV
# urlpatterns = [path('', home, name = 'home'),
#     path('contacts/', contacts, name = 'contacts'),
#     path('products/', prod_list, name = 'products'),
#     path('products/<int:pk>/', prod_one, name = 'one_prod')]