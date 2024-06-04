from typing import Any
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import *
from datetime import datetime


class PostList(ListView):
    model = Post
    ordering = 'date_post'
    context_object_name = 'posts'
    template_name = 'post/news_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_news'] = None
        return context


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post/post_detail.html'
    #queryset = Post.objects.get(pk=pk)