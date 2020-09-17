from django.contrib import admin
from django.urls import path,include

# media
from django.conf.urls.static import static
from django.views.static import serve
from drf_blog.settings import MEDIA_ROOT,MEDIA_URL


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('course.urls')),
    path('markdownx/',include('markdownx.urls')),
    path('comments/',include('django_comments.urls')),
]+static(MEDIA_URL,document_root=MEDIA_ROOT)  #media