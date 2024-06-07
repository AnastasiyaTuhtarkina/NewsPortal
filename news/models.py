from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

class Author(models.Model):
    author = models.OneToOneField(User, on_delete= models.CASCADE)
    author_rating = models.FloatField(default= 0.0)

    def update_rating(self):
        p_rating = self.post_set.aggregate(postRating = Sum('rating_post'))
        p_rat = 0
        p_rat += p_rating.get('postRating')

        c_rating = self.author.comment_set.aggregate(commentRating= Sum('comment_rating'))
        c_rat = 0
        c_rat += c_rating.get('commentRating') or 0

        self.author_rating = p_rat * 3 + c_rat
        self.save()

    def __str__(self):
        return self.author
    
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique= True)

    def __str__(self):
        return self.name_category
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'



class Post(models.Model):
    article = 'AR'
    news = 'NW'

    TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey(Author, on_delete= models.CASCADE)
    type_post = models.CharField(max_length=2, choices= TYPES, default= news) 
    date_post = models.DateTimeField(auto_now_add= True)
    categories_post = models.ManyToManyField(Category, through= 'PostCategory')
    name_post = models.CharField(max_length=255)
    text_post = models.TextField()
    rating_post = models.SmallIntegerField(default= 0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        if self.rating_post != 0:
            self.rating_post -= 1
            self.save()    

    def preview(self):
        return self.text_post[0:123] + '...'    

    def __str__(self):
        return self.name_post
    
    def get_absolute_url(self):
        return reverse('post' , args=[str(self.id)])
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, blank= True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, blank= True)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete= models.CASCADE, blank= True) 
    comment_user = models.ForeignKey(User, on_delete= models.CASCADE, blank= True)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add= True)
    comment_rating = models.SmallIntegerField(default= 0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        if self.comment_rating != 0:
            self.comment_rating -= 1
            self.save()   

    #def __str__(self):
    #    return self.comment_user
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'        