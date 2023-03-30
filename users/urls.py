from django.urls import path
from . import views

urlpatterns = [
    path('userReg/', views.UserRegister.as_view()),
]
