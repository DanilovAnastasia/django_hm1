from django.urls import path

from catalog.apps import CatalogConfig
# from catalog.views import home, contacts, product
from catalog.views import ProductListView, ProductDetailView, ContactsPageView

app_name = CatalogConfig.name

urlpatterns = [
    # path('', home, name='home'),
    # path('contacts/', contacts, name='contacts'),
    # path('product/<int:pk>', product, name='product')
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product')
]
