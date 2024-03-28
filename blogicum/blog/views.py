from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category
from .constants import POST_COUNT_LIMIT


def base_query_set(model_manager=Post.objects):
    """Базовый запрос"""
    queryset = (model_manager.all().
                select_related('category', 'location', 'author').
                filter(is_published=True, category__is_published=True,
                       pub_date__lte=timezone.now()))
    return queryset


def index(request):
    """Индекс"""
    post_list = base_query_set()[:POST_COUNT_LIMIT]
    return render(request, 'blog/index.html', context={'post_list': post_list})


def post_detail(request, pk):
    """Детальное описание"""
    post = get_object_or_404(
        base_query_set(),
        id=pk
    )
    return render(request, 'blog/detail.html', context={'post': post})


def category_posts(request, category_slug):
    """Категория"""
    cur_category = get_object_or_404(
        Category.objects.all().filter(is_published=True, slug=category_slug)
    )
    post_list = base_query_set(cur_category.posts.all())
    return render(request, 'blog/category.html',
                  context={'post_list': post_list, 'category': cur_category})



