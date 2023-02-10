from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group, User
from .forms import PostForm
from .utils import get_page


def index(request):
    posts = Post.objects.select_related('author', 'group')
    context = {
        'page_obj': get_page(
            posts, request.GET.get('page'),
            settings.NUMBER_OF_POSTS_PER_PAGE,
        ),
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    context = {
        'group': group,
        'page_obj': get_page(
            group.posts.all(), request.GET.get('page'),
            settings.NUMBER_OF_POSTS_PER_PAGE,
        ),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    context = {
        'author': author,
        'page_obj': get_page(
            author.posts.all(), request.GET.get('page'),
            settings.NUMBER_OF_POSTS_PER_PAGE,
        ),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        create_post = form.save(commit=False)
        create_post.author = request.user
        create_post.save()
        return redirect('posts:profile', create_post.author)
    title = 'Добавить запись'
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    edit_post = get_object_or_404(Post, id=post_id)
    if request.user != edit_post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=edit_post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    title = 'Редактировать запись'
    context = {
        'form': form, 'post': edit_post, 'title': title,
    }
    return render(request, 'posts/create_post.html', context)
