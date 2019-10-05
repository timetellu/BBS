from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from geetest import GeetestLib
from apps.blog import forms, models
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
# Create your views here.

# VALID_CODE = ""


# 自己生成验证码的登录
# def login(request):
#     # if request.is_ajax():  # 如果是AJAX请求
#     if request.method == "POST":
#         # 初始化一个给AJAX返回的数据
#         ret = {"status": 0, "msg": ""}
#         # 从提交过来的数据中 取到用户名和密码
#         username = request.POST.get("username")
#         pwd = request.POST.get("password")
#         valid_code = request.POST.get("valid_code")  # 获取用户填写的验证码
#         print(valid_code)
#         print("用户输入的验证码".center(120, "="))
#         if valid_code and valid_code.upper() == request.session.get("valid_code", "").upper():
#             # 验证码正确
#             # 利用auth模块做用户名和密码的校验
#             user = auth.authenticate(username=username, password=pwd)
#             if user:
#                 # 用户名密码正确
#                 # 给用户做登录
#                 auth.login(request, user)
#                 ret["msg"] = "/index/"
#             else:
#                 # 用户名密码错误
#                 ret["status"] = 1
#                 ret["msg"] = "用户名或密码错误！"
#         else:
#             ret["status"] = 1
#             ret["msg"] = "验证码错误"
#
#         return JsonResponse(ret)
#     return render(request, "login.html")


# 使用极验滑动验证码的登录

def login(request):
    # if request.is_ajax():  # 如果是AJAX请求
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(username=username, password=pwd)
            if user:
                # 用户名密码正确
                # 给用户做登录
                auth.login(request, user)         #将登录成功的用户，把request.user赋值为登录的用户对象
                ret["msg"] = "/index/"
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)
    return render(request, "login2.html")


#注销
def logout(request):
    auth.logout(request)
    return redirect("/index/")

#首页
def index(request):
    article_list = models.Article.objects.all()
    return render(request, "index.html", {"article_list":article_list})


#获取验证码图片的视图
# def get_valid_img(request):
#     # with open("valid_code.png", "rb") as f:
#     #     data = f.read()
#     # 自己生成一个图片
#     from PIL import Image, ImageDraw, ImageFont
#     import random
#
#     # 获取随机颜色的函数
#     def get_random_color():
#         return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
#
#     # 生成一个图片对象
#     img_obj = Image.new(
#         'RGB',
#         (220, 35),
#         get_random_color()
#     )
#     # 在生成的图片上写字符
#     # 生成一个图片画笔对象
#     draw_obj = ImageDraw.Draw(img_obj)
#     # 加载字体文件， 得到一个字体对象
#     font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
#     # 开始生成随机字符串并且写到图片上
#     tmp_list = []
#     for i in range(5):
#         u = chr(random.randint(65, 90))  # 生成大写字母
#         l = chr(random.randint(97, 122))  # 生成小写字母
#         n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型
#
#         tmp = random.choice([u, l, n])
#         tmp_list.append(tmp)
#         draw_obj.text((20+40*i, 0), tmp, fill=get_random_color(), font=font_obj)
#
#     print("".join(tmp_list))
#     print("生成的验证码".center(120, "="))
#     # 不能保存到全局变量
#     # global VALID_CODE
#     # VALID_CODE = "".join(tmp_list)
#
#     # 保存到session
#     request.session["valid_code"] = "".join(tmp_list)
#     # 加干扰线
#     # width = 220  # 图片宽度（防止越界）
#     # height = 35
#     # for i in range(5):
#     #     x1 = random.randint(0, width)
#     #     x2 = random.randint(0, width)
#     #     y1 = random.randint(0, height)
#     #     y2 = random.randint(0, height)
#     #     draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
#     #
#     # # 加干扰点
#     # for i in range(40):
#     #     draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
#     #     x = random.randint(0, width)
#     #     y = random.randint(0, height)
#     #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())
#
#     # 将生成的图片保存在磁盘上
#     # with open("s10.png", "wb") as f:
#     #     img_obj.save(f, "png")
#     # # 把刚才生成的图片返回给页面
#     # with open("s10.png", "rb") as f:
#     #     data = f.read()
#
#     # 不需要在硬盘上保存文件，直接在内存中加载就可以
#     from io import BytesIO
#     io_obj = BytesIO()
#     # 将生成的图片数据保存在io对象中
#     img_obj.save(io_obj, "png")
#     # 从io对象里面取上一步保存的数据
#     data = io_obj.getvalue()
#     return HttpResponse(data)


#请在官网申请ID使用，示例ID不可使用

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"

# 处理极验 获取验证码的视图
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 注册的视图函数
def register(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        print(request.POST)
        # 帮我做校验
        if form_obj.is_valid():
            # 校验通过，去数据库创建一个新的用户
            form_obj.cleaned_data.pop("re_password")
            avatar_img = request.FILES.get("avatar")
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret["msg"] = "/index/"
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            print(ret)
            print("=" * 120)
            return JsonResponse(ret)
    # 生成一个form对象
    form_obj = forms.RegForm()
    print(form_obj.fields)
    return render(request, "register.html", {"form_obj": form_obj})


#校验用户名是否已存在的接口函数
@csrf_exempt
def check_username_exist(request):
    ret = {"status":0,"msg":""}
    username = request.POST.get("username")
    is_exist = models.UserInfo.objects.filter(username = username)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "用户名已存在，请重新输入"
    return JsonResponse(ret)


#个人博客主页
def home(request,username):
    # print(username)
    user = models.UserInfo.objects.filter(username = username).first()
    if not user:
        return HttpResponse("404")
    blog_obj = user.blog
    #我的文章列表
    article_list =  models.Article.objects.filter(user = user)
    # 我的文章分类及每个分类下文章数      #将我的文章按照我的分类分组，并统计出每个分类下面的文章数
    category_list = models.Category.objects.filter(blog = blog_obj).annotate(c=Count("article")).values("title", "c")
    tag_list = models.Tag.objects.filter(blog = blog_obj).annotate(c=Count("article")).values("title", "c")
    archive_list = models.Article.objects.filter(user = user).extra(
        select={"archive_ym":"date_format(create_time,'%%Y-%%m')"}
    ).values("archive_ym").annotate(c= Count("nid")).values("archive_ym","c")

    return render(request, "home.html",
                  {
                   "username":username,
                   "blog_obj":blog_obj,
                   "article_list":article_list,
                   }
                  )


#文章详情
def article_detail(request,username,pk):
    # print(username,pk)
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    blog_obj = user.blog
    article_obj = models.Article.objects.filter(pk=pk).first()
    comment_list = models.Comment.objects.filter(article_id= pk)
    return render(request,
                  "article_detail.html",
                  {
                      "username":username,
                      "article":article_obj,
                      "blog_obj": blog_obj,
                      "comment_list":comment_list

                   }
                  )


#点赞
from django.db.models import F
def up_down(request):
    print(request.POST)
    article_id=request.POST.get('article_id')
    is_up=json.loads(request.POST.get('is_up'))
    user=request.user
    response={"state":True}
    print("is_up",is_up)
    try:
        models.ArticleUpDown.objects.create(user=user, article_id=article_id, is_up=is_up)
        if is_up:
            models.Article.objects.filter(pk=article_id).update(up_count=F("up_count") + 1)
        else:
            models.Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)

    except Exception as e:
        response["state"]=False
        response["fisrt_action"]= models.ArticleUpDown.objects.filter(user=user, article_id=article_id).first().is_up

    return JsonResponse(response)
    #return HttpResponse(json.dumps(response))


#评论
def comment(request):
    print(request.POST)
    article_id = request.POST.get("article_id")
    content = request.POST.get("content")
    pid = request.POST.get("pid")  #根评论默认为Null
    user_pk = request.user.pk
    response={}

    if not pid:   #根评论
        comment_obj = models.Comment.objects.create(article_id=article_id, content=content, user_id = user_pk)
    else:       #子评论
        comment_obj = models.Comment.objects.create(article_id=article_id, content=content, user_id = user_pk, parent_comment_id=pid)
        response["p_name"] = comment_obj.parent_comment.user.username
        response["p_content"] = comment_obj.parent_comment.content
#这是当前的评论，可以是根评论，也可以是子评论，负责页面刷新后评论列表的显示
    response["create_time"] = comment_obj.create_time.strftime("%Y-%m-%d")
    response["username"]=comment_obj.user.username
    response["content"]=comment_obj.content

    return JsonResponse(response)


#评论树
def comment_tree(request,article_id):

    ret=list(models.Comment.objects.filter(article_id=article_id).values("pk", "content", "parent_comment_id"))
    print(ret)
    return JsonResponse(ret,safe=False)


#添加文章（富文本编辑器 + BS4）
def add_article(request):
    if request.method == "POST":
        title=request.POST.get('title')
        article_content=request.POST.get('article_content')
        user=request.user

        from bs4 import BeautifulSoup
        bs=BeautifulSoup(article_content,"html.parser")
        desc=bs.text[0:150]+"..."

        # 过滤非法标签（防止xss攻击）
        for tag in bs.find_all():
            # print(tag.name)
            if tag.name in ["script", "link"]:
                tag.decompose()

        article_obj= models.Article.objects.create(user=user, title=title, desc=desc)
        models.ArticleDetail.objects.create(content=str(bs), article=article_obj)
        return HttpResponse("添加成功")
    return render(request, "add_article.html")


#文件上传
from bbs import settings
import os,json
def upload(request):
    print(request.FILES)
    obj = request.FILES.get("upload_img")   #文件句柄
    # print("name",obj.name)
    #拿到文件路径
    path=os.path.join(settings.MEDIA_ROOT,"add_article_img",obj.name)  #绝对路径

    #下载（把上传的文件传到指定路径）
    with open(path,"wb") as f:
        for line in obj:
            f.write(line)
    #返回结果：json格式的文件路径
    res={
        "error":0,
        "url":"/media/add_article_img/"+obj.name   #直接作为url输入即可显示
    }
    return HttpResponse(json.dumps(res))    # uploadJson:"/upload/",