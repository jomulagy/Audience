from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('main/', views.main_view, name='main_view'),
    path('search/<str:keyword>/<str:category>/<str:board_type>/<str:post_type>/<str:search_type>/', views.search_page,
         name='search_page'),
    path('search/<str:category>/<str:board_type>/<str:post_type>/<str:search_type>/', views.post_list_page,
         name='post_list_page'),
    path('search/posts/keyword/', views.search_posts, name='search_posts'),
    path('search/posts/', views.post_list, name='post_list'),
    path("total_pages/",views.total_page,name = "total_page")
    # category: 구인/구직, board_type: Free or not, post_type: 구인 -> 관심 분야/신입/경력, search_type: 검색 조건
]
