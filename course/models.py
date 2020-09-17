from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
import os

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255,verbose_name='分类')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="分类"
        verbose_name_plural = verbose_name

class UserDetail(models.Model):
    name = models.CharField(max_length=30,verbose_name='本名')
    length = models.IntegerField(verbose_name='身高')
    sex = models.CharField(max_length=2,verbose_name='性别')
    detail = models.TextField(verbose_name='用户简介')
    email = models.CharField(max_length=50,verbose_name='邮箱')
    img = models.ImageField(upload_to='user',verbose_name='头像')
    user = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    class Meta:
        verbose_name="个人简介"
        verbose_name_plural = verbose_name


# 使用uuid存储图片到media下
def article_img_path(instance,filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8],ext)
    # return '{0}/{1}/{2}'.format(instance.user.id,"avatar",filename)
    return os.path.join('avator',filename)

class Article(models.Model):
    title = models.CharField(max_length=50,verbose_name='文章标题')
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    img = models.ImageField(upload_to=article_img_path,null=True,blank=True,verbose_name='文章配图')
    content = MarkdownxField(verbose_name='内容')
    abstract = MarkdownxField(verbose_name='摘要',null=True,max_length=255)
    visited = models.PositiveIntegerField(verbose_name='访问量',default=0)
    category = models.ManyToManyField('Category',verbose_name='文章分类')
    tags = TaggableManager(verbose_name='标签')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
        verbose_name="文章内容"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    # 可以通过调用这个函数，直接返回详情页的url地址
    def get_absolute_url(self):
        return reverse("app:detail",kwargs={'a_id':self.id})

    # 访问量+1
    def increase_visited(self):
        self.visited += 1
        self.save(update_fields=['visited'])

    # 将markdown转化为html
    def get_markdowm(self):
        return markdownify(self.content)