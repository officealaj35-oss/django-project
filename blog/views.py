from django.http import HttpResponse


def index(request):
    return render(request, 'blog/index.html')


from django.shortcuts import render

# Create your views here.
