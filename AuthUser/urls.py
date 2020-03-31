from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.check_if_logged, name="check"),
    path('create_account/', views.create_account, name="create-account"),
    path('logout/', views.logout, name="logout"),
    path('login/', auth_views.LoginView.as_view(template_name='AuthUser/login.html'), name="login")
]

