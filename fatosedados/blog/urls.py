from django.urls import path
from django.shortcuts import render
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('contato/', views.contato, name='contato'),
    path('sobre/', views.sobre, name='sobre'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    path('termos/', views.termos, name='termos'),
    path('privacidade/', views.privacidade, name='privacidade'),

    path('blog/posts/', views.post_list, name='post_list'),
    path('blog/post/<int:post_id>/<str:title_post>', views.post, name='post'),
    path('blog/post/create/', views.create_post, name='create_post'),
    path('blog/post/edit/<int:post_id>', views.post_edit, name='post_edit'),
    path('blog/post/delete/<int:post_id>', views.post_delete, name='post_delete'),

    # ----------- PAINEL - POST METRICS -----------
    path('blog/post-mertics/', views.post_mertics, name='post_mertics'),

    # ----------- API PAINEL - POST METRICS -----------
    path('api/post-mertics/', views.api_post_metrics, name='api_post_metrics'),
]

if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)