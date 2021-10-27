from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import markdown2
from django import forms
import random

from . import util

class SearchForm(forms.Form):
    Search_Wiki = forms.CharField()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def pages(request, title):
    entries = [page.lower() for page in util.list_entries()]

    if title.lower() in entries:
        file = util.get_entry(title)
        htmlfile = markdown2.markdown(file)
        return render(request, "encyclopedia/pages.html", {
            "title": title,
            "body": htmlfile,
        })
    else:
        return render(request, "encyclopedia/fnferror.html")

def searchpage(request):
    keyword = request.POST.get("q", "")
    valid_entries = [page.lower() for page in util.list_entries()]
    if keyword.lower() in valid_entries:
        index = valid_entries.index(keyword.lower())
        return redirect("wiki:pages", util.list_entries()[index])
    else:
        found_entries = []
        for entry in util.list_entries():
            if keyword.lower() in entry.lower(): found_entries.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": found_entries
        })

def newentry(request):
    return render(request, "encyclopedia/newentry.html")

def saveentry(request):
    title = request.POST.get("t", "")
    content = request.POST.get("content","")
    if title.lower() in [entry.lower() for entry in util.list_entries()]:
        return HttpResponse("Cannot save page. Page already exists")
    with open(f"entries/{title}.md", "w") as file:
        file.write(content)
    return redirect("wiki:pages", title)

def editpage(request):
    title = request.POST.get("title", "")
    with open(f"entries/{title}.md", "r") as readfile:
        content = readfile.read()
    
    return render(request, "encyclopedia/editpage.html", {"content": content, "title": title})

def savechanges(request):
    title = request.POST.get("title", "")
    content = request.POST.get("editedContent", "")
    util.save_entry(title, content)
    return redirect("wiki:pages", title)
    
def randompage(request):
    title = random.choice(util.list_entries())
    return redirect("wiki:pages", title)