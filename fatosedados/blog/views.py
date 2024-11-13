from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.cache import never_cache

from .models import Post, PostImage

def home(request):
    posts = Post.objects.all().order_by("-number_of_visitors")
    addtional_images = PostImage.objects.all()

    latest_posts = Post.objects.all()[:3]
    
    return render(request, 'blog/post_list.html', {'posts': posts, 'addtional_images': addtional_images, 'latest_posts': latest_posts})

def post_list(request):
    posts = Post.objects.all().order_by("-number_of_visitors")
    addtional_images = PostImage.objects.all()

    latest_posts = Post.objects.all()[:3]
    
    return render(request, 'blog/post_list.html', {'posts': posts, 'addtional_images': addtional_images, 'latest_posts': latest_posts})

# @never_cache
def post(request, post_id, title_post):

    if request.method == "GET":

        postFilter = Post.objects.all().filter(id=post_id).first()
        postFilter.number_of_visitors += 1
        postFilter.save()
        
        return render(request, 'blog/post.html', context={'post': postFilter})
    else:
        return JsonResponse({"statusCode": 400, "msg": "not found"})


# ------------------------------------ REVISAR ESSA ALTERNATIVA ------------------------------------
# @never_cache
# def post(request, post_id, title_post):
#     if request.method == "GET":
#         # Checa na sessão se o post já foi visualizado
#         if f"viewed_post_{post_id}" not in request.session:
#             postFilter = Post.objects.all().filter(id=post_id).first()
#             postFilter.number_of_visitors += 1
#             postFilter.save()
            
#             # Marca o post como visualizado na sessão
#             request.session[f"viewed_post_{post_id}"] = True

#         # Pega o post para renderização
#         postFilter = Post.objects.all().filter(id=post_id).first()
#         return render(request, 'blog/post.html', context={'post': postFilter})
    
#     return JsonResponse({"statusCode": 400, "msg": "not found"})



