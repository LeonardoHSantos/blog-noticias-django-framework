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
    # path('blog/post/create/', views.create_post, name='create_post'),
    path('blog/post/create/', views.create_post_v2, name='create_post'),
    path('blog/post/edit/<int:post_id>', views.post_edit, name='post_edit'),
    path('blog/post/delete/<int:post_id>', views.post_delete, name='post_delete'),
    
    # ---- GOOGLE ADS
    path('ads.txt', views.ads_txt_view, name='ads_txt'),


    # ----------- PAINEL - POST METRICS -----------
    path('blog/post-mertics/', views.post_mertics, name='post_mertics'),

    # -----------  APIs -----------
    path('api/v1/login/', views.login_api_v1, name='login_api_v1'),
    path('api/v1/check-user/<str:username>/<str:password>', views.api_check_user_v1, name='api_check_user_v1'),
    path('api/post-mertics/', views.api_post_metrics, name='api_post_metrics'),
    path('api/post-like/', views.api_post_like, name='api_post_like'),

    # GROQ
    path('api/groq/v1/generate-post-text-with-groq-IA/', views.api_v1_generate_post_text_with_groq_IA, name='api_v1_generate_post_text_with_groq_IA'),

]

if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)