import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import redirect
from posts.models import Post, Group, Comment
from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm


# Главная страница
def index(request):
    template = "posts/index.html"
    post_list = Post.objects.all().order_by('-created')
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    context = {
        'page_number': page_number,
        'page_obj': page_obj,
    }
    return render(request, template, context)


# Страница с постами, отфильтрованными по группам
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    posts = Post.objects.filter(group=group).order_by('-created')
    # Показывать по 10 записей на странице.
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')

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
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('posts:index')

@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, pk=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)
