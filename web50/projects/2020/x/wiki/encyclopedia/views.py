from django.shortcuts import render
from django.http import HttpResponseNotFound

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entries = util.get_entry(title)
    if not entries:
        return HttpResponseNotFound()

    return render(request, "encyclopedia/entry.html" , {
        "title" : title,
        "entries" : util.get_entry(title) 
    })