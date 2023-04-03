from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect

from .models import *
from .forms import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('postList')
        else:
            error_message = 'Invalid login credentials'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


# def logout_view(request):
#     logout(request)
#     return redirect('home')


# @login_required
# def home(request):
#     username = request.user
#     context = {
#         'username': username,
#     }
#     return render(request,  'home.html', context)


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})


@csrf_protect
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def insertPost(request):
    # posts = Post.objects.all()
    posts = Post.objects.filter(state=True)

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {'form': form, 'posts': posts}
    return render(request, 'form-post.html', context)


# @login_required
# def postList(request):
#     # posts = Post.objects.all()
#     posts = Post.objects.filter(state=True)

#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#         return redirect('/')
#     context = {'form': form, 'posts': posts}
#     return render(request, 'index.html', context)


@login_required
def postList(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PostForm()

    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(state=True, title__icontains=query)
    else:
        posts = Post.objects.filter(state=True)

    # Paginación
    paginator = Paginator(posts, 6)  # 10 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'form': form, 'page_obj': page_obj}
    return render(request, 'index.html', context)


@login_required
def post(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post': post}
    return render(request, 'post.html', context)


@login_required
def editPost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {'form': form}
    return render(request, 'form-post.html', context)


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        if query:
            results = Post.objects.filter(title__icontains=query)
            context = {'results': results, 'query': query}
            return render(request, 'search.html', context)

    return redirect('postList')


def all_projects(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)  # Mostrar 10 publicaciones por página

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Si el número de página no es un entero, mostrar la primera página.
        posts = paginator.page(1)
    except EmptyPage:
        # Si el número de página está fuera de rango (por ejemplo, 9999),
        # mostrar la última página de resultados.
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
    }
    return render(request, 'all_projects.html', context)


# def post(request, pk):
#     post = Post.objects.get(id=pk)
#     context={'post':post}
#     return render(request, 'Posts/post.html',context)

# def formulario(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')


#     context={'form':form}
#     return render(request, 'posts/form_post.html', context)

# def deletePost (request,pk):
#     post = Post.objects.get(id=pk)
#     if request.method == 'POST':
#         post.delete()
#         return redirect('home')

#     context = {'post':post}

#     return render(request,'delete_template.html', context)

# def updatePost(request,pk):
#     post = Post.objects.get(id=pk)
#     form = PostForm(instance=post)
#     update = 1

#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance = post)
#         form.save()
#         return redirect('home')

#     context = {"form":form, "update":update}
#     return render(request,'posts/form_post.html', context)

# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, 'post_list.html', {'posts': posts})
