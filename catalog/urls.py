from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home
from catalog.views import contacts
from catalog.views import prod_list
from catalog.views import prod_one

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name = 'home'),
    path('contacts/', contacts, name = 'contacts'),
    path('products/', prod_list, name = 'products'),
    path('products/<int:pk>/', prod_one, name = 'one_prod')
]