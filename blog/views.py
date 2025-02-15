from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag
from .forms import PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'categories': categories, 'tags': tags})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return  redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})


def posts_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts, 'category': category})

def posts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag).order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts, 'tag': tag})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'post': post})
