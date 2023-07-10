from django.urls import path
from . import views as views

urlpatterns = [
    path('create/', views.create_comment, name='create_comment'),
    path('update/', views.update_comment, name='create_update'),
    path('delete/', views.delete_comment, name='delete_comment'),
    path('reply/create/', views.create_reply, name='create_reply'),
    path('reply/update/', views.update_reply, name='update_reply'),
    path('reply/delete/', views.delete_reply, name='delete_reply'),
]
