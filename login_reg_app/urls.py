from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_page),
    path('login', views.login_user),
    path('register', views.register_new_user),
    path('success', views.success),
    path('logout', views.logout_user),
]