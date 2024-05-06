from django.urls import path

from catalog.apps import CatalogConfig
# from catalog.views import home, contacts, product
from catalog.views import ProductListView, ProductDetailView, ContactsPageView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    # path('', home, name='home'),
    # path('contacts/', contacts, name='contacts'),
    # path('product/<int:pk>', product, name='product')
    path('', ProductListView.as_view(), name='products_list'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    # Путь для вывода страницы при создании нового объекта
    path('product/', ProductCreateView.as_view(), name='create'),
    # Путь для вывода страницы редактирования продукта
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='update'),
    # Путь для вывода страницы c удалением продукта
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete')
]
