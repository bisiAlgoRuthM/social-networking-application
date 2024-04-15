from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('<int:user_id>/home/', views.home, name='home'),
    path('gemihome', views.gemihome, name='gemihome')
]
