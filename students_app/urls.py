from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('home/', views.home, name='home'),

    path('logout/', views.user_logout, name='logout'),

    # ✅ CRUD URLs
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),

    # 📍 Nearby
    path('nearby/', views.nearby, name='nearby'),
    path('get-nearby/', views.get_nearby_places, name='get_nearby'),
]