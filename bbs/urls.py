"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
# from django.contrib import admin  注释admin
from apps.blog import views, urls as blog_urls
from django.views.static import serve
from django.conf import settings

#以下四句为新添加内容
import xadmin
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.register_models()


urlpatterns = [
    # url(r'^admin/', admin.site.urls),  注释原路由
    url(r'^xadmin/', xadmin.site.urls),  # 添加新路由
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^reg/', views.register),
    url(r'^index/', views.index),

    # url(r'^get_valid_img.png/', views.get_valid_img),

    # 极验滑动验证码 获取验证码的url
    url(r'^pc-geetest/register', views.get_geetest),

    url(r'^check_username_exist/$', views.check_username_exist),

    # media相关的路由设置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

    #将所有blog开头的url都交给app下面的urls.py
    url(r'^blog/', include(blog_urls)),

    url(r'^upload/', views.upload),

]
