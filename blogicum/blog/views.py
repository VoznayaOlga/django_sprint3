from typing import Union

from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from blog.models import Post, Category


def index(request):
    """Индекс"""
    post_list = base_query_set(
        model=Post,
        select_related=['category'],
        filter_={'is_published': True,
                 'category__is_published': True,
                 'pub_date__lte': timezone.now()})[:settings.POST_COUNT_LIMIT]
    return render(request, 'blog/index.html', context={'post_list': post_list})


def post_detail(request, pk):
    """Детальное описание"""
    post = get_object_or_404(
        base_query_set(model=Post,
                       filter_={'is_published': True,
                                'category__is_published': True,
                                'pub_date__lte': timezone.now(),
                                'pk': pk}),
        id=pk
    )
    return render(request, 'blog/detail.html', context={'post': post})


def category_posts(request, category_slug):
    """Категория"""
    cur_category = get_object_or_404(
        base_query_set(
            model=Category,
            filter_={'is_published': True,
                     'slug': category_slug})
    )

    post_list = base_query_set(
        model=Post,
        filter_={'is_published': True,
                 'category': cur_category,
                 'pub_date__lte': timezone.now()})
    return render(request, 'blog/category.html',
                  context={'post_list': post_list, 'category': cur_category})


# Ниже эксперимент по созданию базового запроса
def base_query_set(model, values: Union[str, None] = None,
                   filter_: Union[dict, None] = None,
                   select_related: Union[list[str], None] = None):
    """Базовый запрос"""
    if select_related is not None:
        queryset = model.objects
        for item in select_related:
            queryset = queryset.select_related(item)
    else:
        queryset = model.objects.all()

    if values is not None:
        queryset = queryset.values(values)
    if filter_ is not None:
        filtered = {k: v for k, v in filter_.items() if v}
        queryset = queryset.filter(**filtered)
    return queryset
