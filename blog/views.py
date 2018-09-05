from django.contrib import messages, auth
from django.core.mail import mail_admins
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse

from django_blog.helpers import pg_records
from .models import Author, Category, Tag, Post
from .forms import FeedbackForm


def post_list(request):
    posts = Post.objects.order_by('-id').all()
    posts = pg_records(request, posts, 5)

    ctx = {
        'posts': posts
    }
    return render(request, 'blog/post_list.html', ctx)


def post_detail(request, pk, post_slug):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    ctx = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', ctx)


def post_by_category(request, category_slug):
    # category = Category.objects.get(slug=category_slug)
    # posts = Post.objects.filter(category__slug=category_slug)
    category = get_object_or_404(Category, slug=category_slug)
    # posts = get_list_or_404(Post, category=category)
    posts = get_list_or_404(Post.objects.order_by('-id'), category=category)
    posts = pg_records(request, posts, 5)
    ctx = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog/post_by_category.html', ctx)


def post_by_tag(request, tag_slug):
    # tag = Tag.objects.get(slug=tag_slug)
    # posts = Post.objects.filter(tags__slug=tag_slug)
    # posts = Post.objects.filter(tags__name=tag)
    tag = get_object_or_404(Tag, slug=tag_slug)
    # posts = get_list_or_404(Post, tags=tag)
    posts = get_list_or_404(Post.objects.order_by('-id'), tags=tag)
    posts = pg_records(request, posts, 5)
    ctx = {
        'tag': tag,
        'posts': posts
    }
    return render(request, 'blog/post_by_tag.html', ctx)


def feedback(request):
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            sender = form.cleaned_data['email']
            subject = "You have a new Feedback from {}:{}".format(name, sender)
            message = "Subject: {}\n\nMessage: {}".format(form.cleaned_data['subject'],
                                                          form.cleaned_data['message'])
            mail_admins(subject, message)

            form.save()
            messages.add_message(request, messages.INFO,
                                 'Feedback submitted')
            return redirect('blog:feedback')
    else:
        form = FeedbackForm()
    ctx = {
        'form': form
    }
    return render(request, 'blog/feedback.html', ctx)


def tracker_user(request):
    response = render(request, 'blog/track_user.html')
    if not request.COOKIES.get('visits'):
        response.set_cookie('visits', '1', 3600 * 24 * 365 * 2)
    else:
        visits = int(request.COOKIES.get('visits', '1')) + 1
        response.set_cookie('visits', str(visits), 3600 * 24 * 365 * 2)
    return response


def stop_tracking(request):
    if request.COOKIES.get('visits'):
       response = HttpResponse("Cookies Cleared")
       response.delete_cookie("visits")
    else:
        response = HttpResponse("We are not tracking you.")
    return response


def login(request):
    if request.user.is_authenticated():
        return redirect('blog:admin_page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('blog:admin_page')
        else:
            messages.error(request, "Error wrong username/password")
    return render(request, 'blog/login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'blog/logout.html')


def admin_page(request):
    if not request.user.is_authenticated():
        return redirect('blog:blog_login')
    return render(request, 'blog/admin_page.html')
