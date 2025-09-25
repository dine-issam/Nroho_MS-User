from django.urls import path
from . import views

urlpatterns = [
    path('',views.getData),
    path('create',views.addUser),
    path ('fetch/<str:pk>', views.getUser),
    path ('update/<str:pk>', views.updateUser),
    path ('delete/<str:pk>', views.deleteUser),
    path("signup",views.signup),
    path("signin",views.signin)
    
]
