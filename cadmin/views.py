import smtplib
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse, get_object_or_404, Http404

from blog.forms import PostForm, CategoryForm, TagForm
from blog.models import Author, Tag, Category, Post
from django_blog import helpers
from .forms import CustomUserCreationForm


@login_required
def home(request):
    # if not request.user.is_authenticated():
    #     return redirect('cadmin:login')
    return render(request, 'cadmin/admin_page.html')


def register(request):
    print(request.scheme)
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            activation_key = helpers.generate_activation_key(
                username=request.POST['username'])
            
            subject = 'TheGreatDjangoBlog Account Verification'
            message = '''\n
                         Please visit the following link to verify your account 
                         \n\n{0}://{1}/cadmin/activate/account/?key={2}
                        '''.format(request.scheme, request.get_host(), activation_key)

            error = False

            try:
                print(request.POST['email'])
                send_mail(subject, message, settings.SERVER_EMAIL, [request.POST['email']], fail_silently=False)
                messages.add_message(request, messages.INFO,
                                     'Account created! Click on the link sent to your email to activate the account')
            except:   # smtplib.SMTPException as Error
                error = True
                messages.add_message(request, messages.INFO,
                                     'Unable to send email verification. Please try again')
            
            if not error:
                user = User.objects.create_user(
                    request.POST['username'],
                    request.POST['email'],
                    request.POST['password1'],
                    is_active = 0,
                    is_staff = True
                )

                author = Author()
                author.activation_key = activation_key
                author.user = user
                author.save()
            # form.save()
            # messages.success(request, 'Account created successfully')
            return redirect('cadmin:register')
    else:
        # form = UserCreationForm()
        form = CustomUserCreationForm()
    ctx = {
        'form': form,
    }
    return render(request, 'cadmin/register.html', ctx)


def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('cadmin:home')
    else:
        return auth_views.login(request, **kwargs)


def activate_account(request):
    key = request.GET['key']
    if not key:
         raise Http404()
    result = get_object_or_404(Author, activation_key=key,
                               email_validated=False)
    result.user.is_active = True
    result.user.save()
    result.email_validated = True
    result.save()

    return render(request, 'cadmin/activated.html')


@login_required
def account_info(request):
    return render(request, 'cadmin/account_info.html')


@login_required
def post_add(request):
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # if author is not selected and user is superuser, 
            # then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                new_post = form.save(commit=False)
                author = Author.objects.get(user__username='staff')
                new_post.author = author
                new_post.save()
                form.save_m2m()
            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                new_post = form.save()
            # if user is not a superuser
            else:
                new_post = form.save(commit=False)
                author = Author.objects.get(user__username=request.user.username)
                new_post.author = author
                new_post.save()
                form.save_m2m()
            messages.add_message(request, messages.INFO, 'Post added')
            return redirect('cadmin:post_add')
    else:
        form = PostForm()
    ctx = {
        'form': form,
    }
    return render(request, 'cadmin/post_add.html', ctx)


@login_required
def post_update(request, pk):
    
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        print(request.POST)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # if author is not selected and user is superuser, 
            # then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                updated_post = form.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_post.author = author
                updated_post.save()
                form.save_m2m()
            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                updated_post = form.save()
            # if user is not a superuser
            else:
                updated_post = form.save(commit=False)
                author = Author.objects.get(user__username=request.user.username)
                updated_post.author = author
                updated_post.save()
                form.save_m2m()
            messages.add_message(request, messages.INFO, 'Post updated')
            return redirect(reverse('cadmin:post_update', args=[post.id]))
    else:
        form = PostForm(instance=post)
    ctx = {
        'form': form,
        'post': post,
    }
    return render(request, 'cadmin/post_update.html', ctx)


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Post deleted')
    return redirect(next_page)


@login_required
def post_list(request):
    if request.user.is_superuser:
        posts = Post.objects.order_by("-id").all()
    else:
        posts = Post.objects.filter(author__user__username=request.user.username).order_by("-id")
    posts = helpers.pg_records(request, posts, 5)
    ctx = {
        'posts': posts,
    }
    return render(request, 'cadmin/post_list.html', ctx)


@login_required
def category_list(request):
    if request.user.is_superuser:
        categories = Category.objects.order_by("-id").all()
    else:
        categories = Category.objects.filter(author__user__username=request.user.username).order_by("-id")

    categories = helpers.pg_records(request, categories, 5)

    ctx = {
        'categories': categories
    }
    return render(request, 'cadmin/category_list.html', ctx)


@login_required
def category_add(request):

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        form = CategoryForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if form.is_valid():
            # new_category = form.save()
            # new_category = form.save(commit=False)
            # new_category.author = get_user(request)
            # new_category.save()

            if request.POST.get('author') == "" and request.user.is_superuser:
                # if author is not supplied and user is superuser
                new_category = form.save(commit=False)
                author = Author.objects.get(user__username='staff')
                new_category.author = author
                new_category.save()
            elif request.POST.get('author') and request.user.is_superuser:
                # if author is supplied and user is superuser
                new_category = form.save()
            else:
                # if author not a superuser
                new_category = form.save(commit=False)
                new_category.author = Author.objects.get(user__username=request.user.username)
                new_category.save()

            messages.add_message(request, messages.INFO, 'Category added')
            return redirect('cadmin:category_add')

    # if request is GET the show unbound form to the user
    else:
        form = CategoryForm()

    ctx = {
        'form': form,
    }
    return render(request, 'cadmin/category_add.html', ctx)


# view to update category
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST": # If request is POST, create a bound form
        form = CategoryForm(request.POST, instance=category)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the category form

        # If form is invalid show form with errors again
        if form.is_valid():

            if request.POST.get('author') == "" and request.user.is_superuser:
                # if author is not supplied and user is superuser
                updated_category = form.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_category.author = author
                updated_category.save()
            elif request.POST.get('author') and request.user.is_superuser:
                # if author is supplied and user is superuser
                updated_category = form.save()
            else:
                # if author not a superuser
                updated_category = form.save(commit=False)
                updated_category.author = Author.objects.get(user__username=request.user.username)
                updated_category.save()

            new_category = form.save()
            messages.add_message(request, messages.INFO, 'Category updated')
            return redirect(reverse('cadmin:category_update', args=[category.id]))

    # if request is GET the show unbound form to the user
    else:
        form = CategoryForm(instance=category)

    ctx = {
        'form': f,
        'category': category
    }
    return render(request, 'cadmin/category_update.html', ctx)


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Category deleted')
    return redirect(next_page)


@login_required
def tag_list(request):
    if request.user.is_superuser:
        tags = Tag.objects.order_by("-id").all()
    else:
        tags = Tag.objects.filter(author__user__username=request.user.username).order_by("-id")

    tags = helpers.pg_records(request, tags, 5)
    ctx = {
        'tags': tags
    }
    return render(request, 'cadmin/tag_list.html', ctx)


# view to add new tag
@login_required
def tag_add(request):

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        form = TagForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if form.is_valid():
            # new_category = form.save()
            # new_category = form.save(commit=False)
            # new_category.author = get_user(request)
            # new_category.save()

            if request.POST.get('author') == "" and request.user.is_superuser:
                # if author is not supplied and user is superuser
                new_tag = form.save(commit=False)
                author = Author.objects.get(user__username='staff')
                new_tag.author = author
                new_tag.save()
            elif request.POST.get('author') and request.user.is_superuser:
                # if author is supplied and user is superuser
                new_tag = form.save()
            else:
                # if author not a superuser
                new_tag = form.save(commit=False)
                new_tag.author = Author.objects.get(user__username=request.user.username)
                new_tag.save()

            messages.add_message(request, messages.INFO, 'Tag added')
            return redirect('tag_add')

    # if request is GET the show unbound form to the user
    else:
        form = TagForm()

    ctx = {
        'form': form,
    }
    return render(request, 'cadmin/tag_add.html', ctx)


# view to update tag
@login_required
def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST": # If request is POST, create a bound form
        form = TagForm(request.POST, instance=tag)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the tag update form

        # If form is invalid show form with errors again
        if form.is_valid():
            # updated_tag = form.save()

            if request.POST.get('author') == "" and request.user.is_superuser:
                # if author is not supplied and user is superuser
                updated_tag = form.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_tag.author = author
                updated_tag.save()
            elif request.POST.get('author') and request.user.is_superuser:
                # if author is supplied and user is superuser
                updated_tag = form.save()
            else:
                # if author not a superuser
                updated_tag = form.save(commit=False)
                updated_tag.author = Author.objects.get(user__username=request.user.username)
                updated_tag.save()

            messages.add_message(request, messages.INFO, 'Tag updated')
            return redirect(reverse('tag_update', args=[tag.id]))

    # if request is GET the show unbound form to the user
    else:
        form = TagForm(instance=tag)

    ctx = {
        'form': form,
        'tag': tag
    }
    return render(request, 'cadmin/tag_update.html', ctx)


@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Tag deleted')
    return redirect(next_page)
