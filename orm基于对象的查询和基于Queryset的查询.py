import os


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bbs.settings")

    import django
    django.setup()

    from apps.blog import models

    # 基于对象的查询 SQL: 子查询
    # a1 = models.Article.objects.first()
    # print(a1.user.avatar, type(a1.user))

# 基于QuerySet查询, SQL: join连表查询
    # a2 = models.Article.objects.filter(pk=1)
    # print(a2.values("user__avatar"))


    # 查询a1对应的评论数
    ret = models.Article.objects.all().first()
    print(ret,type(ret))

