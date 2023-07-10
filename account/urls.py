from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='account_login'),
    path('applicant/create/', views.ApplicantCreateView.as_view(), name='create_applicant'),
    path('employer/create/', views.EmployerCreateView.as_view(), name='create_employer'),
    path('username/search/', views.search_username, name='search_username'),
    path('password/search/', views.search_password, name='search_password'),
    path('detail/', views.account_detail, name='account_detail'),
    path('password/check/', views.check_password, name='check_password'),
    path('password/update/', views.change_password, name='update_password'),
    path('update/', views.AccountUpdateView.as_view(), name='update_account'),
    path('delete/', views.delete_account, name='delete_account'),
    path('posts/', views.my_posts, name='my_posts'),
    path('posts/detail/', views.my_posts_detail, name='my_posts_detail'),
    path('signup/finish/', views.signup_finish, name='signup_finish'),
]
