from django.db import models

import os
from datetime import datetime

def upload_to_cover(instance, filename):
    # Define o diretório para a imagem principal
    dt = datetime.now()
    year = dt.year
    month = dt.month
    day = dt.day

    dirname = f"{year}/{month}/{day}"
    next_id = Post.objects.all()
    
    if next_id.filter(id=instance.id).first():
        next_id = next_id.filter(id=instance.id).first().pk
    else:
        next_id = len(next_id) + 1
    return os.path.join('post_images_principal', f'{dirname}/{next_id}', filename)

def upload_to_additional(instance, filename):
    # Define o diretório para as imagens adicionais
    dt = datetime.now()
    year = dt.year
    month = dt.month
    day = dt.day
    dirname = f"{year}/{month}/{day}"

    next_id = Post.objects.all()
    next_id = next_id.filter(id=instance).first()
    if next_id:
        next_id = next_id.pk
    else:
        next_id = len(next_id) + 1
    return os.path.join('post_images_post', f'{dirname}/{next_id}', filename)

class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to=upload_to_cover, blank=True, null=True)  # Imagem principal do post
    number_of_visitors = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to_additional )  # Outras imagens do post

    def __str__(self):
        return f"Imagem para {self.post.title}"
