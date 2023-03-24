from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid login credentials'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def home(request):
    username = request.user
    context = {
        'username': username,
    }
    return render(request,  'home.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@csrf_protect
def logout_view(request):
    logout(request)
    return redirect('login')


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
