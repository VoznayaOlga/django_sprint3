"""Блог"""
import datetime

from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category


def index(request):
    """Индекс"""
    template = 'blog/index.html'
    post_list = Post.objects.select_related('category').filter(
        is_published=True,
        category__is_published=True,
        pub_date__date__lte=datetime.date.today()
    ).order_by('-pub_date')[0:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, pk):
    """Детальное описание"""
    template = 'blog/detail.html'
    post = get_object_or_404(Post.objects.all().filter(
        is_published=True, category__is_published=True,
        pub_date__date__lte=datetime.date.today(),
        pk=pk
    ))
    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    """Категория"""
    template = 'blog/category.html'
    cur_category = get_object_or_404(Category.objects.all().filter(
        is_published=True, slug=category_slug)
    )
    post_list = Post.objects.select_related('category').filter(
        is_published=True, category=cur_category,
        pub_date__date__lte=datetime.date.today()
    ).order_by('-pub_date')
    context = {'post_list': post_list, 'category': cur_category}
    return render(request, template, context)
