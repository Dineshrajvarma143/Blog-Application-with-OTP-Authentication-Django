from django.urls  import path
from .views import create_user,login_user,verify_otp,home,create_blog,logout_user,update_blog,delete_blog
urlpatterns = [
    path('',create_user,name='registeruser'),
    path('l',login_user,name='loginuser'),
    path('otp',verify_otp,name='verify_otp'),
    path('home',home,name='home'),
    path('create',create_blog,name='create'),
    path('logout',logout_user,name='logout'),
    path('update/<int:id>/',update_blog, name='update'),
    path('delete/<int:id>/', delete_blog, name='delete'),

]
