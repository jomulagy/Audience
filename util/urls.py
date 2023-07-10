from django.urls import path
from . import views

urlpatterns = [
    path('like/create/', views.add_like, name='add_like'),
    path('dislike/create/', views.add_dislike, name='add_dislike'),
]
