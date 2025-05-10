from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return HttpResponseNotFound()

    return render(request, "encyclopedia/entry.html" , {
        "title" : title,
        "entry" : entry 
    })

def search(request):
    query = request.GET.get("q")
    #print(f"query: {query}, Type: {type(query)}")
    entry = util.get_entry(query)

    if not entry :
        # 정확히 일치하는 게 없다면, substring이 일치하는 목록 보여주기
        results = []
        for filename in util.list_entries():
            #print(f"filename: {filename}")
            if query.lower() in filename.lower():
                results.append(filename)

        return render(request, "encyclopedia/search.html", {
            "results" : results
        })
        
    else:
        # 정확히 일치하는게 있으면 그 entry로 redirect
        return HttpResponseRedirect(reverse("entry", args=[query]))