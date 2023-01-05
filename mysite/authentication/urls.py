from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_form,name="login_form"),
    path('logout/',views.logout_form,name="logout_form"),
    path('register/',views.register_form,name="register_form"),
]  