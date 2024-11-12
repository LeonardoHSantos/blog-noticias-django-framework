from django.shortcuts import render
from .models import Post, PostImage

def post_list(request):
    posts = Post.objects.all()
    addtional_images = PostImage.objects.all()

    latest_posts = Post.objects.all()[:3]
    
    return render(request, 'blog/post_list.html', {'posts': posts, 'addtional_images': addtional_images, 'latest_posts': latest_posts})

def post(request, post_id):
    postFilter = Post.objects.all().filter(
        id=post_id
    ).first()
    print(postFilter.title)
    # addtional_images = PostImage.objects.all()
    return render(request, 'blog/post.html', context={'post': postFilter})


