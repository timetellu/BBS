from django.conf.urls import url
from apps.blog import views

urlpatterns = [
    url(r"backend/add_article/", views.add_article),
    url(r'comment/', views.comment),
    url(r'up_down/', views.up_down),
    url(r"comment_tree/(\d+)/", views.comment_tree),

    url(r'(\w+)/article/(\d+)/$', views.article_detail),   #文章详情
    url(r'(\w+)/$', views.home),


    ]