import xadmin
from apps.blog import models       # from .models import *


# Register your models here.
#因为之前已经在admin中注册过，所以应该先注销
xadmin.site.unregister(models.UserInfo)
# 注册表
xadmin.site.register(models.UserInfo)
xadmin.site.register(models.Article)
xadmin.site.register(models.Blog)
xadmin.site.register(models.Tag)
xadmin.site.register(models.Category)
xadmin.site.register(models.Comment)
xadmin.site.register(models.ArticleUpDown)
xadmin.site.register(models.ArticleDetail)
xadmin.site.register(models.Article2Tag)
