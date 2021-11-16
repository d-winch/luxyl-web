from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {"context_variable": "hello"}
    return render(request, 'index.html', context)