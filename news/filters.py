from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter
from .models import Post, Category
from django.forms import DateInput


class PostFilter(FilterSet):

    # def __init__(self, *args, **kwargs):
    #     super(PostFilter, self).__init__(*args, **kwargs)
    #     self.filters['name'].label = 'Имя'

    class Meta:
       model = Post
       fields = {
           'name_post': ['icontains'],
       }
   
    category = ModelMultipleChoiceFilter(
        field_name = 'categories_post',
        queryset = Category.objects.all(),
        label = 'categories_post'
    )

    date_post_after = DateFilter(
        field_name='date_post',
        lookup_expr='date__gte',
        widget=DateInput(
            attrs={'type':'date'},
        )
    )


class PostSearch(FilterSet):

    class Meta:
       model = Post
       fields = {
           'name_post': ['icontains'],
       }
   
    category = ModelMultipleChoiceFilter(
        field_name = 'categories_post',
        queryset = Category.objects.all(),
        label = 'categories_post'
    )

    date_post_after = DateFilter(
        field_name='date_post',
        lookup_expr='date__gte',
        widget=DateInput(
            attrs={'type':'date'},
        )
    )

   