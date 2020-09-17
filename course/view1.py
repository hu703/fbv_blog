from django.shortcuts import render,HttpResponse
from .models import *
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django_comments.models import Comment

# 第三方
import markdown,pygments
from taggit.models import Tag
from blog.settings import EMAIL_HOST_USER,EMAIL_FROM


# 搜索
def search(request):
    if request.method == 'POST':
        con_get = request.POST.get('con')
        tags = Tag.objects.all()
        name = User.objects.filter(username__contains=con_get).all()  # 作者
        article = Article.objects.filter(title__contains=con_get).all()  # 文章标题
        if article: 
            all_art = article
        if name:
            all_art = Article.objects.filter(author=name[0].id).all()
        articles = Article.objects.all()
        articles_list = articles[:3]
        # 最新评论
        comment_list = Comment.objects.all()
        return render(request,'search.html',{'articles':all_art,'tags':tags,'articles_list':articles_list,'con_get':con_get,'comment_list':comment_list})

# 首页
def index(request):
    articles = Article.objects.all()
    # 分页
    limit = 1
    paginator = Paginator(articles,limit)
    page = request.GET.get('page',1)
    loaded = paginator.page(page)
    # 获取全部标签
    tags = Tag.objects.all()
    # 最新评论
    comment_list = Comment.objects.all()
    # 最新文章
    articles_list = articles[:3]
    return render(request,'index.html',{'articles':loaded,'tags':tags,'articles_list':articles_list,'comment_list':comment_list})

# 分类
def category(request,c_id):
    cate = Category.objects.get(id=c_id)
    name = cate.name
    articles = cate.article_set.all()
    tags = Tag.objects.all()

    articles = Article.objects.all()
    articles_list = articles[:3]
     # 最新评论
    comment_list = Comment.objects.all()
    return render(request,'category.html',{'articles':articles,'name':name,'tags':tags,'articles_list':articles_list,'comment_list':comment_list})

# 标签
def tags(request,t_id):
    li = []
    cate = Tag.objects.get(id=t_id)
    name = cate.name
    aa = Article.objects.all()
    for i in aa:
        for ai in i.tags.all():
            if str(ai) == str(name):
                li.append(i)
    tags = Tag.objects.all()
    articles = Article.objects.all()
    articles_list = articles[:3]
     # 最新评论
    comment_list = Comment.objects.all()
    return render(request,'tags.html',{'articles':li,'name':name,'tags':tags,'articles_list':articles_list,'comment_list':comment_list})

#作者
def author(request,u_id):
    name = User.objects.get(id=u_id)
    articles = Article.objects.filter(author=u_id).all()
    user_detail = UserDetail.objects.filter(user=u_id).all()
    if user_detail:
        userdeta = user_detail[0]
    return render(request,'author.html',{'articles':articles,'name':name.username,'userdeta':userdeta})

# 详情页
def detail(request,a_id):
    single_article = Article.objects.get(id=a_id)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',  #扩展
        'markdown.extensions.codehilite', #高亮
        'markdown.extensions.toc',  #目录
    ])
    tags = single_article.tags.all()
    # 展示为html
    single_article.content = md.convert(single_article.content)
    single_article.abstract = md.convert(single_article.abstract)
    single_article.toc= md.toc # 目录
    single_article.increase_visited() # 调用models的函数，增加访问量
    # 获取全部标签
    tags_all = Tag.objects.all()
    articles = Article.objects.all()
    articles_list = articles[:3]
     # 最新评论
    comment_list = Comment.objects.all()
    return render(request,'single_article.html',{'single_article':single_article,'tags':tags,'tags_all':tags_all,'articles_list':articles_list,'comment_list':comment_list})


# 关于我
def about(request):
    return render(request,'about.html')

# 联系我
def contact(request):
    if request.method == 'POST':
        name_get = request.POST.get('name')
        from_email2 = request.POST.get('email')
        subject = request.POST.get('theme')
        con_get = request.POST.get('con')
        html_message = "<div><p>博主，你好呀，我是{}, 我对您的博客非常的感兴趣，并向你提出一下问题：</p>{}</div>".format(name_get,con_get)
        # recipient_list = [EMAIL_HOST_USER]
        # send_mail(subject,message,from_email,recipient_list)
        from_email = EMAIL_FROM   # 发件人邮箱
        recipient_list = [from_email2]  # 收件人邮箱列表
        message='正文'
        # 发送邮箱
        send_mail(subject,message,from_email,recipient_list,html_message=html_message)
        return render(request,'contact.html',{'ok':"邮件发送成功..."})
    return render(request,'contact.html')