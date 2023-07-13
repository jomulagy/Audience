from django.urls import path
from . import views as views

app_name = "employ"
urlpatterns = [
    path('<int:post_id>/', views.employ_post_detail, name='employ_post_detail'),
    path('create/', views.create_employ_post, name='create_employ_post'),
    path('update/<int:id>/',views.update_employ_post,name='update_employ_post'),
    path('delete/<int:id>/',views.delete_employ_post,name='delete_employ_post'),
    path('freepost/<int:post_id>/', views.employ_free_post_detail, name='employ_free_post_detail'),
    path('freepost/create/', views.create_employ_free_post, name='create_employ_free_post'),
    path('freepost/update/<int:id>/',views.update_employ_free_post,name='update_employ_free_post'),
    path('freepost/delete/<int:id>/',views.delete_employ_free_post,name='delete_employ_free_post'),
    path("question/list/", views.QA_list_data, name = "QA_list_data"),
    path("question/list/<int:id>", views.QA_list, name = "QA_list"),
    path('question/create/<int:post_id>/', views.create_question, name='create_question'),
    path('question/<int:post_id>/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/delete/<int:post_id>/',views.delete_question,name='delete_question'),
    path('answer/create/<int:post_id>/<int:question_id>/', views.create_answer, name='create_answer'),
    path('answer/delete/<int:post_id>/<int:question_id>/',views.delete_answer,name='delete_answer'),
    path("report/create/", views.report_create_e, name = "report_create_e"),

]
