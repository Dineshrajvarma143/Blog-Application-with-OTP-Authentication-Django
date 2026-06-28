from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('',                  RedirectView.as_view(url='/home/'), name='index'),
    path('home/',             views.home,          name='home'),
    path('blog/<int:id>/',    views.blog_detail,   name='blog_detail'),
    path('registeruser/',     views.register_user, name='register_user'),
    path('login/',            views.login_user,    name='login'),
    path('verify-otp/',       views.verify_otp,    name='verify_otp'),
    path('resend-otp/',       views.resend_otp,    name='resend_otp'),
    path('create/',           views.create_blog,   name='create'),
    path('update/<int:id>/',  views.update_blog,   name='update'),
    path('delete/<int:id>/',  views.delete_blog,   name='delete'),
    path('profile/update/',   views.update_profile, name='update_profile'),
    path('logout/',           views.logout_user,   name='logout'),
]