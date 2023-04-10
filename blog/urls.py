from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView
                    )


urlpatterns = [
    path('', PostListView.as_view(),name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(),name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(),name='post-detail'),
    path('post/new/', PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(),name='post-delete'),
    path('about/',views.about, name='blog-about'),
    
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#<app>/<model>_<viewtype>.html