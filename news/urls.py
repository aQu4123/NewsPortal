from django.urls import path
# Импортируем созданные нами представления
from .views import PostsList, PostDetail, PostSearch, PostCreate, PostDelete, PostEdit

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('create/', PostCreate.as_view(), name='news_create'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
   path('article/create/', PostCreate.as_view(), name='article_create'),
   path('article/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
   path('article/<int:pk>/edit/', PostEdit.as_view(), name='article_edit'),
]
