from django.shortcuts import render
from django.http import HttpResponse


def index(request, name="Julius"):
    String = 'Simple is better than complex' 
    context = {"name": name, "nums": [1, 2, 3, 4, 5], "string": String}
    return render(request, 'myapp/hello.html', context)