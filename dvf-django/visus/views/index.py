from django.shortcuts import render
from django.template import loader
# Create your views here.
from django.http import HttpResponse

from .backend import visus

def index(request):
    template = loader.get_template("index.html")
    context = {
        "visus": visus
    }
    return HttpResponse(template.render(context, request))

