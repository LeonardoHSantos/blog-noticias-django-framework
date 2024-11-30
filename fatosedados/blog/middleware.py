from django.urls import resolve, Resolver404
from django.shortcuts import render

class VerificarURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            resolve(request.path_info)
        except Resolver404:
            # Tratar a URL inexistente aqui
            return render(request, '404.html', status=404)

        response = self.get_response(request)
        return response