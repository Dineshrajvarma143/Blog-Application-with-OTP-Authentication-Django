from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Blog
import random


# ─── Helper: Generate & send OTP ───────────────────────────────────────────
def generate_otp():
    return str(random.randint(100000, 999999))
    print(f"🔐 OTP generated: {otp}")
    return otp

def send_otp_email(email, otp):
    subject = 'Your Inkwell OTP Verification Code'
    message = f'''
Hi,

Your OTP for Inkwell Blog is: {otp}

This code is valid for 5 minutes. Do not share it with anyone.

– Inkwell Team
'''
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)


# ─── Register ──────────────────────────────────────────────────────────────
def register_user(request):
    if request.method == 'POST':
        fname     = request.POST.get('fname', '').strip()
        lname     = request.POST.get('lname', '').strip()
        email     = request.POST.get('email', '').strip()
        password  = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # Validations
        if not all([fname, lname, email, password, password2]):
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'register.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'register.html')

        # Store data in session and send OTP
        otp = generate_otp()
        request.session['reg_data'] = {
            'fname': fname, 'lname': lname,
            'email': email, 'password': password,
        }
        request.session['otp'] = otp
        request.session['otp_purpose'] = 'register'

        try:
            send_otp_email(email, otp)
        except Exception:
            messages.error(request, 'Failed to send OTP. Check your email settings.')
            return render(request, 'register.html')

        messages.success(request, f'OTP sent to {email}')
        return redirect('verify_otp')

    return render(request, 'register.html')


# ─── Login ─────────────────────────────────────────────────────────────────
def login_user(request):
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')

        # Send OTP for 2FA
        otp = generate_otp()
        request.session['otp'] = otp
        request.session['otp_purpose'] = 'login'
        request.session['login_email'] = email

        try:
            send_otp_email(email, otp)
        except Exception:
            messages.error(request, 'Failed to send OTP. Check your email settings.')
            return render(request, 'login.html')

        messages.success(request, f'OTP sent to {email}')
        return redirect('verify_otp')

    return render(request, 'login.html')


# ─── OTP Verification ──────────────────────────────────────────────────────
def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        session_otp = request.session.get('otp')
        purpose     = request.session.get('otp_purpose')

        if not session_otp:
            messages.error(request, 'OTP expired. Please try again.')
            return redirect('login')

        if entered_otp != session_otp:
            messages.error(request, 'Incorrect OTP. Please try again.')
            return render(request, 'verify_otp.html')

        # OTP is correct
        if purpose == 'register':
            data = request.session.get('reg_data', {})
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['fname'],
                last_name=data['lname'],
            )
            login(request, user)
            # Cleanup session
            for key in ['otp', 'otp_purpose', 'reg_data']:
                request.session.pop(key, None)
            messages.success(request, f'Welcome, {user.first_name}! Account created successfully.')
            return redirect('home')

        elif purpose == 'login':
            email = request.session.get('login_email')
            user  = User.objects.get(username=email)
            login(request, user)
            for key in ['otp', 'otp_purpose', 'login_email']:
                request.session.pop(key, None)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('home')

    # GET request — show OTP page
    email = (
        request.session.get('login_email') or
        request.session.get('reg_data', {}).get('email', '')
    )
    return render(request, 'verify_otp.html', {'email': email})


# ─── Resend OTP ────────────────────────────────────────────────────────────
def resend_otp(request):
    purpose = request.session.get('otp_purpose')
    if purpose == 'login':
        email = request.session.get('login_email')
    else:
        email = request.session.get('reg_data', {}).get('email')

    if not email:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('login')

    otp = generate_otp()
    request.session['otp'] = otp

    try:
        send_otp_email(email, otp)
        messages.success(request, 'New OTP sent successfully!')
    except Exception:
        messages.error(request, 'Failed to resend OTP.')

    return redirect('verify_otp')


# ─── Home ──────────────────────────────────────────────────────────────────
def home(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'blogs': blogs})


# ─── Create Blog ───────────────────────────────────────────────────────────
@login_required(login_url='login')
def create_blog(request):
    if request.method == 'POST':
        title   = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if not title or not content:
            messages.error(request, 'Title and content are required.')
            return render(request, 'create.html')

        Blog.objects.create(
            title=title,
            content=content,
            author=request.user,
        )
        messages.success(request, 'Blog post published successfully!')
        return redirect('home')

    return render(request, 'create.html')


# ─── Update Blog ───────────────────────────────────────────────────────────
@login_required(login_url='login')
def update_blog(request, id):
    blog = get_object_or_404(Blog, id=id)

    # Only the author can edit
    if blog.author != request.user:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('home')

    if request.method == 'POST':
        title   = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if not title or not content:
            messages.error(request, 'Title and content are required.')
            return render(request, 'update.html', {'blog': blog})

        blog.title   = title
        blog.content = content
        blog.save()
        messages.success(request, 'Blog post updated successfully!')
        return redirect('home')

    return render(request, 'update.html', {'blog': blog})


# ─── Delete Blog ───────────────────────────────────────────────────────────
@login_required(login_url='login')
def delete_blog(request, id):
    blog = get_object_or_404(Blog, id=id)

    # Only the author can delete
    if blog.author != request.user:
        messages.error(request, 'You are not authorized to delete this post.')
        return redirect('home')

    blog.delete()
    messages.success(request, 'Blog post deleted.')
    return redirect('home')


# ─── Logout ────────────────────────────────────────────────────────────────
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')