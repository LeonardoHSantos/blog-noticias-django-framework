import os
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.conf import settings


POST_CATEGORIES = (
    ("uncategorized", "Selecione uma categotia"),
    ("Technology", "Tecnologia"),
    ("Economy", "Economia"),
    ("Policy", "Política"),
    ("Health", "Saúde"),
    ("Education", "Educação"),
    ("Environment", "Meio Ambiente"),
    ("Science", "Ciência"),
    ("Sports", "Esportes"),
    ("Entertainment", "Entretenimento"),
    ("Lifestyle", "Estilo de Vida"),
)

class UserRegistrationManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("O usuário deve ter um email")
        if not name:
            raise ValueError("O usuário deve ter um nome")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            last_login=timezone.now(),  # Define o last_login como o momento atual
            date_joined=timezone.now()  # Define o date_joined como o momento atual
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class UserRegistration(AbstractBaseUser):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Para permitir login no admin
    is_superuser = models.BooleanField(default=False)

    objects = UserRegistrationManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Contato de {self.name} - {self.email} em {self.created_at.strftime('%Y-%m-%d %H:%M')}"





def upload_to_cover(instance, filename, instante_id=False):
    # Define o diretório para a imagem principal
    dt = datetime.now()
    year = dt.year
    month = dt.month
    day = dt.day
    dirname = f"{year}\{month}\{day}"

    if instante_id:
        next_id = instance.pk
    else:
        next_id = Post.objects.all()
        if next_id.filter(id=instance.id).first():
            next_id = next_id.filter(id=instance.id).first().pk
        else:
            next_id = len(next_id) + 1
    
    return os.path.join('post_images_principal', f'{dirname}\{next_id}', filename)

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
    content = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to=upload_to_cover, blank=True, null=True)  # Imagem principal do post
    number_of_visitors = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category = models.CharField(max_length=125, blank=False, null=False, default="uncategorized")

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to_additional )  # Outras imagens do post

    def __str__(self):
        return f"Imagem para {self.post.title}"



# ------------------------ Like and Comment - POST ------------------------
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    action = models.CharField(default="", max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



# ------------------------ PAINEL -POST  METRICS------------------------
class PostMetrics(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='metrics')
    access_datetime = models.DateTimeField(default=datetime.now)
    
    class Meta:
        verbose_name = "Post Metric"
        verbose_name_plural = "Posts Metrics"

    def __str__(self):
        return f"Metric for {self.post.title} on {self.access_datetime}"
