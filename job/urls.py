from django.urls import path
from . import views as views

app_name = "job"
urlpatterns = [
    path('<int:post_id>/', views.job_post_detail, name='job_post_detail'),
    path('create/', views.create_job_post, name='create_job_post'),
    path('update/<int:id>/',views.update_job_post,name='update_job_post'),
    path('delete/<int:id>/',views.delete_job_post,name='delete_job_post'),
    path('freepost/<int:post_id>/', views.job_free_post_detail, name='job_free_post_detail'),
    path('freepost/create/', views.create_job_free_post, name='create_job_free_post'),
    path('freepost/update/<int:id>/', views.update_job_free_post, name='update_job_free_post'),
    path('freepost/delete/<int:id>/', views.delete_job_free_post, name='delete_job_free_post'),
    path("report/create/", views.report_create_j, name="report_create_j"),
    path("company/search/", views.search_company, name="search_company"),
]
