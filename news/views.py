from typing import Any
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django_filters.views import FilterView
from .forms import PostForm
from django.contrib.auth.decorators import login_required
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

    def get_queryset(self):
       queryset = super().get_queryset()
       self.filterset = PostFilter(self.request.GET, queryset)
       return self.filterset.qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    
class PostSearch(FilterView):    
    model = Post
    ordering = 'date_post'
    filterset_class = PostFilter
    template_name = 'post_search.html'
    context_object_name = 'news'
    paginate_by = 50


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'
    #queryset = Post.objects.get(pk=pk)

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == 'articles/create/':
            post.type_post = 'AR'
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')