from django.shortcuts import render,redirect,get_object_or_404
from .froms import Registerform,Loginform,OTPForm,Createform
from .models import Bloguser,Create_blog
import random
from django.core.mail import send_mail
# Create your views here.
def create_user(request):
    form = Registerform()
    if request.method == "POST":
        form = Registerform(request.POST)
        if form.is_valid():
            form.save()
        return redirect('loginuser')
    return render(request, 'register.html', {
        'form': form
    })

def login_user(request):
    if request.method == "POST":
        form = Loginform(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['registered_email']

            user = Bloguser.objects.filter(
                full_name=full_name,
                registered_email=email
            ).first()

            if user:
                otp = str(random.randint(100000, 999999))

                # Store in session
                request.session['otp'] = otp
                request.session['login_email'] = email

                print("Your OTP is:", otp)

                return redirect("verify_otp")
            else:
                return render(request, "login.html", {
                    "form": form,
                    "error": "Invalid details"
                })
    else:
        form = Loginform()

    return render(request, "login.html", {"form": form})

def verify_otp(request):
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            session_otp = request.session.get('otp')
            if entered_otp == session_otp:
                request.session['user'] = request.session.get('login_email')
                return redirect("home")
            else:
                return render(request, "otp.html", {
                    "form": form,
                    "error": "Invalid OTP"
                })
    else:
        form = OTPForm()

    return render(request, "otp.html", {"form": form})


def home(request):
    if 'user' not in request.session:
        return redirect('loginuser')

    blog = Create_blog.objects.all()
    return render(request,'home.html',{'blogs':blog})


def create_blog(request):
    if 'user' not in request.session:
        return redirect('loginuser')
    form = Createform()
    if request.method == 'POST':
        form = Createform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, "create.html", {"form": form})
from django.shortcuts import redirect

def logout_user(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('loginuser')

def update_blog(request, id):

    blog = get_object_or_404(Create_blog, id=id)

    form = Createform(instance=blog)

    if request.method == "POST":
        form = Createform(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'update.html', {'form': form})
def delete_blog(request, id):
    blog = get_object_or_404(Create_blog, id=id)

    if request.method == "POST":
        blog.delete()
        return redirect('home')
    return render(request, 'delete_confirm.html', {'blog': blog})