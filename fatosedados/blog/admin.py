from django.contrib import admin
from .models import Post, PostImage, Contact, UserRegistration

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Contact)
admin.site.register(UserRegistration)