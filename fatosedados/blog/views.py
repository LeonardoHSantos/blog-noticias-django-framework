from django.shortcuts import render
from .models import Post, PostImage

def post_list(request):
    posts = Post.objects.all()
    addtional_images = PostImage.objects.all()

    # for post in posts:
    #     print(post.cover_image)
    # #     print(post.additional_images)
    return render(request, 'blog/post_list.html', {'posts': posts, 'addtional_images': addtional_images})
