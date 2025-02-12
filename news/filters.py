from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter
from django import forms
from .models import Post, Author

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):

    author = ModelChoiceFilter(
        field_name = 'author',
        queryset = Author.objects.all(),
        label = 'Author',
        empty_label = 'All'
    )
    date_in = DateTimeFilter(
        field_name='date_in',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Поиск по дате',
        lookup_expr='gte',
    )
    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
           # поиск по названию
           'title': ['icontains'],
           # поиск по автору
           # 'author': ['exact']
        }


