import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page

from posts.models import Post, Group, Comment
from django.contrib.auth import get_user_model

# Функция reverse_lazy позволяет получить URL по параметрам функции path()
# Берём, тоже пригодится
from django.urls import reverse_lazy

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import PostForm, CommentForm


# Главная страница
@cache_page(20)
def index(request):
    template = "posts/index.html"
    # keyword = request.GET.get("q", None)
    # logging.info(keyword)
    # if keyword:
    #     posts = Post.objects.filter(text__contains=keyword).select_related('author').select_related('group')
    # else:
    #     posts = None
    # context = {
    #     'posts': posts,
    #     "keyword": keyword,
    # }
    # return render(request, template, context)
    post_list = Post.objects.all().order_by('-created')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядить так:
    # post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


# Страница с постами, отфильтрованными по группам
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    # Метод .filter позволяет ограничить поиск по критериям.
    # Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by('-created')
    # Показывать по 10 записей на странице.
    paginator = Paginator(posts, 10)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    author_posts = Post.objects.filter(author=author).order_by('-created')
    paginator = Paginator(author_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Здесь код запроса к модели и создание словаря контекста
    context = {
        'username': username,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created')
    author = post.author
    author_count_posts = Post.objects.filter(author=author).count()
    form = CommentForm(
        request.POST or None,
    )
    context = {
        'post': post,
        'author_count_posts': author_count_posts,
        'comments': comments,
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def create_post(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=Post(author=request.user)
    )

    if form.is_valid():
        form.save()
        return redirect(f'/profile/{request.user.username}/')

    template_name = 'posts/create_post.html'
    context = {
        'form': form
    }
    return render(request, template_name, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    # Получите пост
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, pk=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)
