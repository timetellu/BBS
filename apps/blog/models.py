from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户信息表
    """
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=True, unique=True,verbose_name="电话")
    avatar = models.FileField(upload_to="media/avatars/", default="avatars/default.png", verbose_name="头像")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    blog = models.OneToOneField(to="Blog", to_field="nid", null=True,verbose_name="博客")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name="用户"
        verbose_name_plural=verbose_name

class Blog(models.Model):
    """
    博客信息
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64,verbose_name="博客标题")  # 个人博客标题
    site = models.CharField(max_length=32, unique=True,verbose_name="博客后缀")  # 个人博客后缀
    theme = models.CharField(max_length=32,verbose_name="博客主题")  # 博客主题

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="BLog站点"
        verbose_name_plural=verbose_name

class Category(models.Model):
    """
    个人博客文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32,verbose_name="分类标题")  # 分类标题
    blog = models.ForeignKey(to="Blog", to_field="nid",verbose_name="关联博客")  # 外键关联博客，一个博客站点可以有多个分类

    def __str__(self):
        return self.title
    class Meta:
        verbose_name="文章分类"
        verbose_name_plural=verbose_name


class Tag(models.Model):
    """
    标签
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32,verbose_name="标签名")  # 标签名
    blog = models.ForeignKey(to="Blog", to_field="nid",verbose_name="所属博客")  # 所属博客

    def __str__(self):
        return self.title
    class Meta:
        verbose_name="标签"
        verbose_name_plural=verbose_name

class Article(models.Model):
    """
    文章
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50,verbose_name="文章标题")  # 文章标题
    desc = models.CharField(max_length=255,verbose_name="文章描述")  # 文章描述
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")     # 创建时间

    # 评论数
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    # 点赞数
    up_count = models.IntegerField(verbose_name="点赞数", default=0)
    # 踩
    down_count = models.IntegerField(verbose_name="踩数", default=0)

    category = models.ForeignKey(to="Category", to_field="nid", null=True,verbose_name="目录")
    user = models.ForeignKey(to="UserInfo", to_field="id",verbose_name="用户")
    tags = models.ManyToManyField(  # 中介模型
        to="Tag",
        through="Article2Tag",
        through_fields=("article", "tag"),  # 注意顺序！！！
        verbose_name="标签"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="文章列表"
        verbose_name_plural=verbose_name

class ArticleDetail(models.Model):
    """
    文章详情表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name="文章内容")
    article = models.OneToOneField(to="Article", to_field="nid",verbose_name="文章")

    class Meta:
        verbose_name="文章详情"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.article.title

class Article2Tag(models.Model):
    """
    文章和标签的多对多关系表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid")
    tag = models.ForeignKey(to="Tag", to_field="nid")

    def __str__(self):
        return "{}-{}".format(self.article.title,self.tag.title)

    class Meta:
        unique_together = (("article", "tag"),)

    class Meta:
        verbose_name="文章-标签"
        verbose_name_plural=verbose_name

class ArticleUpDown(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", null=True,verbose_name="用户")
    article = models.ForeignKey(to="Article", null=True,verbose_name="文章")
    is_up = models.BooleanField(default=True,verbose_name="是否点赞")

    def __str__(self):
        return self.article.title

    class Meta:
        unique_together = (("article", "user"),)
        verbose_name="文章点赞"
        verbose_name_plural=verbose_name

class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid",verbose_name="文章")
    user = models.ForeignKey(to="UserInfo", to_field="id",verbose_name="用户")
    content = models.CharField(max_length=255,verbose_name="评论内容")  # 评论内容
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    parent_comment = models.ForeignKey("self", null=True,blank=True,verbose_name="父评论")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name="评论"
        verbose_name_plural=verbose_name
