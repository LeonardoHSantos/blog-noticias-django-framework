import re
from datetime import datetime

from django.shortcuts import render, redirect
from django.http.response import JsonResponse
# from django.contrib.auth.models import User
# from django.views.decorators.cache import never_cache
from .models import Post, PostImage, Contact, UserRegistration
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.hashers import check_password

def home(request):
    posts = Post.objects.all().order_by("-number_of_visitors")
    addtional_images = PostImage.objects.all()

    latest_posts = Post.objects.all()[:3]
    return render(request, 'blog/post_list.html', {'posts': posts, 'addtional_images': addtional_images, 'latest_posts': latest_posts})

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
            return redirect('login')

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

def post_list(request):
    
    posts = Post.objects.all().order_by("-number_of_visitors")
    addtional_images = PostImage.objects.all()

    latest_posts = Post.objects.all()[:3]
    
    return render(request, 'blog/post_list.html', {'posts': posts, 'addtional_images': addtional_images, 'latest_posts': latest_posts})

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')
        cover_image = request.FILES.get('cover_image')  # Supondo que o campo de imagem esteja no formulário

        if not all([title, author, content]):
            return JsonResponse({"statusCode": 400, "msg": "Todos os campos obrigatórios devem ser preenchidos."})

        post = Post.objects.create(
            title=title,
            author=author,
            content=content,
            cover_image=cover_image,
            created_at=datetime.now()
        )

        return redirect('post_list')  # Redireciona para uma página de sucesso (deve ser ajustada ao seu projeto)
    
    return render(request, 'blog/create_post.html')

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



