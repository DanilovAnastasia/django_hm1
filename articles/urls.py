from django.urls import path

from articles.apps import ArticlesConfig
from articles.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = ArticlesConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='list'),
    path('view/<int:pk>', ArticleDetailView.as_view(), name='view'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('edit/<int:pk>', ArticleUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', ArticleDeleteView.as_view(), name='delete')
]