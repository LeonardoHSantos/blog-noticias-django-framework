from django.urls import path
from django.conf.urls import handler404
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

    path('posts/', views.post_list, name='post_list'),
    path('post/<int:post_id>/<str:title_post>', views.post, name='post'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/edit/<int:post_id>', views.post_edit, name='post_edit'),
    path('post/delete/<int:post_id>', views.post_delete, name='post_delete'),
]


def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404

if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)