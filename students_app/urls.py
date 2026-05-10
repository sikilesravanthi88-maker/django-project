from django.urls import path
from . import views   # ✅ ADD THIS

urlpatterns = [
    path('', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('update/<int:id>/', views.update, name='update'),
    path('logout/', views.user_logout, name='logout'),
]