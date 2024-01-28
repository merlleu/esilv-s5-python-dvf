from django.shortcuts import render
from django.template import loader
# Create your views here.
from django.http import HttpResponse

from .backend import visus

def visu(request):
    template = loader.get_template("visu.html")
    visu_id = int(request.GET["id"])
    for visu in visus:
        if visu["id"] == visu_id:
            break
    if visu["id"] != visu_id:
        raise Exception("Visu not found")
    
    options, selected_choices = extract_chosen_options(visu, request.GET)
    context = {
        "visu": {
            "id": visu["id"],
            "name": visu["name"],
            "options": options
        },
        "visu_html": visu['renderer'](*selected_choices)
    }
    return HttpResponse(template.render(context, request))

def extract_chosen_options(visu, get):
    options = []
    selected_choices = []
    for option in visu["options"]:
        r=get.get(f"opt_{option['id']}")
        if r is None:
            r = 0

        r = int(r)
        if r >= len(option["choices"]):
            raise Exception("Invalid choice")
        i = option["choices"][r]
        
        options.append({
            "id": option["id"],
            "name": option["name"],
            "choice": i['id'],
            "choices": option["choices"]
        })

        selected_choices.append(i['id'])
            

    return options, selected_choices