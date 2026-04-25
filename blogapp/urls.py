from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:id>/', views.detail, name='detail'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]