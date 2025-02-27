# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.urls import reverse
from .tasks import notify_about_new_post

class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'

class PostSearch(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'news_search.html'
    context_object_name = 'news'


    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        # context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == reverse('article_create'):
            post.type = "AR"
        post.save()
        # notify_about_new_post.delay(post.pk)
        return super().form_valid(form)

class PostDelete(DeleteView):
    # permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    # def dispatch(self, request, *args, **kwargs):
    #     post = self.get_object
    #     if self.request.path == reverse('article_delete'):

class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'



from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    # Author.objects.create(user=user)
    return redirect('/news/')

@login_required
def subscribe(request, pk):
    user = request.user
    subscribed = Category.objects.get(pk=pk)
    if not user.subscribers.filter(pk=pk).exists():
        subscribed.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unsubscribe(request, pk):
    user = request.user
    subscribed = Category.objects.get(pk=pk)
    if user.subscribers.filter(pk=pk).exists():
        subscribed.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))


class CategoryList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'news_category.html'
    context_object_name = 'news'
    paginate_by = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.category = Category.objects.get(pk=self.kwargs.get('pk'))
        queryset = queryset.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
