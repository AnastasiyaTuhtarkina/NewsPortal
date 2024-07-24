from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('post/', cache_page(60)(PostList.as_view()), name='post_list'),
    path('post/<int:pk>/', cache_page(60*5)(PostDetail.as_view()), name='post'),
    path('post/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('author_now/', Author_now, name='author_now'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]