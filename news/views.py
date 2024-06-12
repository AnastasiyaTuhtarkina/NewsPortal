from typing import Any
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect

from .models import *
from .forms import PostForm
from .filters import PostFilter


@login_required
def show_protected_page(requests):
    pass

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