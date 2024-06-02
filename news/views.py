from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import *


class PostList(ListView):
    model = Post
    ordering = 'date_post'
    context_object_name = 'posts'
    template_name = 'news/templates/news/post_detail.html'


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'news/templates/news/post_detail.html'
    #queryset = Post.objects.get(pk=pk)