from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http.response import HttpResponse #  импортируем респонс для проверки текста
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef
from django.utils import timezone
from django.views import View

from .translation import PostTranslationOptions
from .models import *
from .forms import PostForm
from .filters import PostFilter

import pytz #  импортируем стандартный модуль для работы с часовыми поясами
 
 
class Index(View):
    def get(self, request):
 
        #.  Translators: This message appears on the home page only
        models = PostTranslationOptions.objects.all()
 
        context = {
            'models': models,
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones #  добавляем в контекст все доступные часовые пояса
        }
        
        return HttpResponse(render(request, 'index.html', context))
 
    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name_category')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

class PostList(ListView):
    model = Post
    ordering = 'date_post'
    context_object_name = 'posts'
    template_name = 'news_list.html'
    paginate_by = 10 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    
class PostSearch(FilterView):    
    model = Post
    ordering = 'date_post'
    filterset_class = PostFilter
    template_name = 'post_search.html'
    context_object_name = 'news'
    paginate_by = 50

    def get_queryset(self):
       queryset = super().get_queryset()
       self.filterset = PostFilter(self.request.GET, queryset)
       return self.filterset.qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'
    #queryset = Post.objects.get(pk=pk)

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj    

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_product',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == 'articles/create/':
            post.type_post = 'AR'
        else:
            post.type_post = 'NW'    
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_product',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_product',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


def Author_now(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        user.groups.add(author_group)
    return redirect(request.META['HTTP_REFERER'])    