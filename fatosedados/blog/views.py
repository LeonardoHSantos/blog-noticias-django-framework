import os
import re
from datetime import datetime

from django.shortcuts import render, redirect
from django.http.response import JsonResponse
# from django.contrib.auth.models import User
# from django.views.decorators.cache import never_cache
from .models import Post, PostImage, Contact, UserRegistration, upload_to_cover
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.hashers import check_password

def home(request):
   posts = Post.objects.all().order_by("-number_of_visitors")[:3]
   addtional_images = PostImage.objects.all()
   latest_posts = Post.objects.all().order_by("-created_at")[:3]
   return render(request, 'blog/home.html', {'posts': posts, 'addtional_images': addtional_images, 'latest_posts': latest_posts})

def contato(request):
    if request.method == "GET":
        return render(request, 'blog/contato.html')
    elif request.method == "POST":
        print(request.POST)
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]
        new_contact = Contact.objects.create(name=name, email=email, message=message)
        
        if new_contact:
            print("contato salvo com sucesso")
            print(new_contact)
            return render(request, 'blog/contato.html', context={"contact_success": True, "msg": "formulário enviado com sucesso"})
        else:
            return render(request, 'blog/contato.html', context={"contact_error": True, "msg": "falha ao enviar formulário de contato"})

        # return redirect('contact')

def sobre(request):
    if request.method == "GET":
        return render(request, 'blog/sobre.html')
    else:
        return JsonResponse({"statusCode": 400, "msg": "not found"})

def login(request):
    if request.method == "GET":
        return render(request, "user/login.html")
    elif request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Usando authenticate para verificar as credenciais com o modelo customizado
        user = authenticate(request, username=email, password=password)
        print("\n\n >>>>>>>>> user")
        print(user)
        if user is not None:
            django_login(request, user)  # Realiza o login
            return redirect('home')
        else:
            print("E-mail ou senha incorretos.")
            context = {
                "email": email,
                "password": password,
                "error_login": True,
                "msg": "Usuário ou senha incorretos."
            }
            return render(request, "user/login.html", context=context )

def logout(request):
    django_logout(request)
    return redirect("login")

def register(request):
    if request.method == "GET":
        return render(request, 'user/register.html')
    
    elif request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

        context = {
            "name": name,
            "email": email,
            "password": password,
            "confirm_password": confirm_password,
        }
        print(context)

        if not re.match(EMAIL_REGEX, email):
            context["message_form"] = True
            context["message_form_list"] = ["Por favor, insira um e-mail válido."]

            return render(request, 'user/register.html', context=context)

        if password == confirm_password:
            if not re.match(PASSWORD_REGEX, password):
                context["message_form"] = True
                context["message_form_list"] = [
                    "Por favor, insira uma senha válida.",
                    " - Deve ter pelo menos 8 caracteres",
                    " - Pelo menos uma letra maiúscula",
                    " - Pelo menos uma letra minúscula",
                    " - Pelo menos um número",
                    " - Pelo menos um caractere especial, exemplo: #, @, %, *, /",
                    ]
                return render(request, 'user/register.html', context=context)
        else:
            context["message_form"] = True
            context["message_form_list"] = [
                "As senhas estão diferentes. Por favor revise."
            ]
            return render(request, 'user/register.html', context=context)
        
        if UserRegistration.objects.filter(email=email).exists():
            context["message_form"] = True
            context["message_form_list"] = ["Este e-mail está indisponível. Tente outro."]
            return render(request, 'blog/register.html', context=context)

        user = UserRegistration.objects.create_user(
            name=name,
            email=email,
            password=password
        )
        user.save()

        context={"message_form_success_save": True}

        return render(request, 'user/register.html', context=context)

    else:
        return JsonResponse({"statusCode": 400, "msg": "not found"})
        

def termos(request):
    return render(request, 'termos_privacidade/termos.html')

def privacidade(request):
    return render(request, 'termos_privacidade/politica.html')

# Renderiza todos os Posts
def post_list(request):
    
    posts = Post.objects.all().order_by("-number_of_visitors")
    
    addtional_images = PostImage.objects.all()

    latest_posts = Post.objects.all().order_by("-created_at")[:3]
    
    return render(request, 'blog/post_list.html', {'posts': posts, 'addtional_images': addtional_images, 'latest_posts': latest_posts})

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')
        cover_image = request.FILES.get('cover_image')  # Supondo que o campo de imagem esteja no formulário

        if not all([title, author, content, cover_image]):
            return JsonResponse({"statusCode": 400, "msg": "Todos os campos obrigatórios devem ser preenchidos."})

        post = Post.objects.create(
            title=title,
            author=author,
            content=content,
            cover_image=cover_image,
            created_at=datetime.now(),
            user=request.user,
        )

        return redirect('post_list')
    
    return render(request, 'blog/create_post.html')
# ---
def remove_images(old_image_dir):
    try:
        # Verifica se o diretório contém imagens e exclui
        if os.path.exists(old_image_dir):   
            for filename in os.listdir(old_image_dir):
                file_path = os.path.join(old_image_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"\n\n Sucesso ao limpar diretório de imagens: {old_image_dir}\n\n")
    except Exception as e:
        print(f"\n\n ERROR REMOVE IMAGES | ERROR: {e}")
        print(f"Diretório: {old_image_dir}")
# ---
def post_edit(request, post_id):

    postFilter = Post.objects.all().filter(id=post_id).first()

    if request.method == "POST":

        title = request.POST.get("title")
        author = request.POST.get("author")
        content = request.POST.get("content")
        cover_image = request.FILES.get('cover_image')

        postFilter.title=title
        postFilter.author=author
        postFilter.content=content

        # Atualiza diretório de imagem apenas se houver alguma imagem no input do formulário HTML.
        if cover_image:
            old_image_path = postFilter.cover_image.path
            old_image_dir = os.path.dirname(old_image_path)
            remove_images(old_image_dir=old_image_dir)
            postFilter.cover_image=cover_image
            print(f"\n\n ------------ IMAGEM ATUALIZADA | ID: {postFilter.pk} ------------ ")
        
        postFilter.save()
   
        return render(request, 'blog/post_edit.html', context={"post": postFilter})
    
    elif request.method == "GET":
        if postFilter.user.id == request.user.pk:
            return render(request, 'blog/post_edit.html', context={"post": postFilter})
        else:
            return render(request, 'blog/post_edit.html', context={"post": {
                "no_access_post": True
            }})
    else:
        return JsonResponse({"404": "not-found"})
# ---
def post_delete(request, post_id):

    postFilter = Post.objects.all().filter(id=post_id).first()
    
    if request.method == "GET":
        if postFilter.user.id == request.user.pk:
            return render(request, 'blog/post_delete.html', context={"post": postFilter})
        else:
            return render(request, 'blog/post_delete.html', context={"post": {
                "no_access_post": True
            }})
    elif request.method == "POST":
        print(postFilter)
        if postFilter.user.id == request.user.pk:
            postFilter.delete()
            print(f" --------------------- POST DELETADO COM SUCESSO --------------------- ")
           
            return render(request, 'blog/post_delete.html', context={"post": {
                "delete_success_post": True
            }})
        else:
            return JsonResponse({"error": "Você não tem permissão para deletar este post."}, status=403)
    
    else:
        return JsonResponse({"404": "not-found"})

def post(request, post_id, title_post):

    if request.method == "GET":

        postFilter = Post.objects.all().filter(id=post_id).first()
        postFilter.number_of_visitors += 1
        postFilter.save()

        print(f">>>> postFilter: {postFilter.created_at}")

        context={
            "post": {
                "id": postFilter.pk,
                "user_id": postFilter.user.id,
                "title": postFilter.title,
                "author": postFilter.author,
                "content": postFilter.content,
                "cover_image": postFilter.cover_image,
                "number_of_visitors": postFilter.number_of_visitors,
                "created_at": postFilter.created_at,
            }
        }

        print(context)
        
        return render(request, 'blog/post.html', context=context)
    else:
        return JsonResponse({"statusCode": 400, "msg": "not found"})


# -------------------- DASHBOARD - POST METRICS --------------------
def post_mertics(request):
    if request.method == "GET":
        return render(request, "metrics/post_metrics.html")

def post_metrics_ranking_top_5(request):
    if request.method == "GET":
        posts = Post.objects.all().order_by("-number_of_visitors")[:5]
        
        titles              = list(map(lambda x: x.title, posts ))
        numbers_of_visitors = list(map(lambda x: x.number_of_visitors, posts ))
        
        return JsonResponse({
            "titles": titles,
            "numbers_of_visitors": numbers_of_visitors,
        })