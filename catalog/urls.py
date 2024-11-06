from catalog.views import home
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView,
    ProductDetailView,
    contacts,
    ProductDeleteView,
    ProductCreateView,
    ProductUpdateView
)

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name="home"),
    path("", ProductListView.as_view(), name="products_list"),
    path("catalog/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('contacts/', contacts, name='contacts'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# вариант CBV
# urlpatterns = [
#     path('', home, name="home"),
#     path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
#     path('menu.html', MenuListView.as_view(), name='menu'),
#     path("products/", ProductListView.as_view(), name="product_list"),
#     path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
#     path("products/create", ProductCreateView.as_view(), name="product_create"),
#     path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
#     path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),


# Изменение продукта для модератора
#     path('moderator-update/<int:pk>/', ModeratorProductUpdateView.as_view(), name='moderator_update_product'),
#     path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),  # Удаление продукта
#     ]


# вариант FBV
# urlpatterns = [path('', home, name = 'home'),
#     path('contacts/', contacts, name = 'contacts'),
#     path('products/', prod_list, name = 'products'),
#     path('products/<int:pk>/', prod_one, name = 'one_prod')]
