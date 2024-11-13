from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:post_id>/<str:title_post>', views.post, name='post'),
]
