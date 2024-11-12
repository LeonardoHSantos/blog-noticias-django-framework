from django.db import models

import os
from django.db import models

def upload_to_cover(instance, filename):
    # Define o diretório para a imagem principal
    return os.path.join('post_images_principal', f'pasta_{instance.id}', filename)

def upload_to_additional(instance, filename):
    # Define o diretório para as imagens adicionais
    return os.path.join('post_images_post', f'pasta_{instance.post.id}', filename)

class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to=upload_to_cover, blank=True, null=True)  # Imagem principal do post

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to_additional )  # Outras imagens do post

    def __str__(self):
        return f"Imagem para {self.post.title}"
