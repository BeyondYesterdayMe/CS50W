from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return HttpResponseNotFound() #HttpResponseBadRequest 가 나은가??

    return render(request, "encyclopedia/entry.html" , {
        "title" : title,
        "entry" : markdown2.markdown(entry) 
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
    
def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title):
            return HttpResponseBadRequest("Already Existed Page")
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
    else:
        return render(request, "encyclopedia/create.html")

def edit(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        entry = request.POST.get("entry")
        print(f"[{title}]")
        print(f"[{entry}]")
        if util.get_entry(title) != entry:
            util.save_entry(title, entry)        
        return HttpResponseRedirect(reverse("entry", args=[title]))
    else:
        title = request.GET.get("title")
        return render(request, "encyclopedia/edit.html", {
            "title" : title,
            "entry" : util.get_entry(title).strip()
        })

def randompage(request):
    entries = util.list_entries()
    if not entries:
        return HttpResponseBadRequest("Empty entries")
    rnd = random.randint(0, len(entries)-1)
    return HttpResponseRedirect(reverse("entry", args=[entries[rnd]]))