from django.shortcuts import render,redirect,get_object_or_404
from .froms import Registerform,Loginform,Createform
from .models import Create_blog
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def create_user(request):
    form = Registerform()
    if request.method == "POST":
        form = Registerform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        form = Loginform(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = Loginform()
    return render(request, "login.html", {"form": form})


@login_required
def home(request):
    blog = Create_blog.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        blog = blog.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(penname__icontains=search_query)
        )
    return render(request,'home.html',{'blogs':blog})

from django.contrib.auth.decorators import login_required
from .models import Bloguser

@login_required
def create_blog(request):
    form = Createform()

    if request.method == "POST":
        form = Createform(request.POST)

        if form.is_valid():
            blog = form.save(commit=False)

            blog_user, created = Bloguser.objects.get_or_create(user=request.user)
            blog.user = blog_user
            blog.save()
            return redirect('home')
    return render(request, "create.html", {"form": form})
from django.shortcuts import redirect


def logout_user(request):
    logout(request)
    return redirect('loginuser')


@login_required
def update_blog(request, id):

    blog = get_object_or_404(Create_blog, id=id)

    form = Createform(instance=blog)

    if request.method == "POST":
        form = Createform(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'update.html', {'form': form})


@login_required
def delete_blog(request, id):
    blog = get_object_or_404(Create_blog, id=id)

    if request.method == "POST":
        blog.delete()
        return redirect('home')
    return render(request, 'delete_confirm.html', {'blog': blog})