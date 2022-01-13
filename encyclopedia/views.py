from django.core.files.storage import default_storage
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
import markdown2
from django.urls import reverse
from django import forms
import random, os

from . import util

class SearchForm(forms.Form):
    Search_Wiki = forms.CharField()

def index(request):
    """returns index page"""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def pages(request, title):
    """
    Renders the requested wepage
    takes title as an arguement to display that particular page
    """
    #fetch list of lowercase entries to check if the requested title is available or not
    entries = [page.lower() for page in util.list_entries()]

    if title.lower() in entries:
        file = util.get_entry(title)
        #convert the fetched .md file to html file
        htmlfile = markdown2.markdown(file)
        return render(request, "encyclopedia/pages.html", {
            "title": title,
            "body": htmlfile,
        })
    else:
        return render(request, "encyclopedia/fnferror.html") #file not found error

def searchpage(request):
    """
    Searches the local storage for existing markdown/entry files and lists them
    typical search function
    """

    #fetch keyword from search box
    keyword = request.POST.get("q", "")
    #list of existing entries in lower case to look for search item
    valid_entries = [page.lower() for page in util.list_entries()]

    # if whole keyword is exists in the entries then render that page
    if keyword.lower() in valid_entries:
        index = valid_entries.index(keyword.lower())
        return redirect("wiki:pages", util.list_entries()[index])
    #else check if the keyword is a substring of the available entries
    else:
        found_entries = []
        for entry in util.list_entries():
            if keyword.lower() in entry.lower(): found_entries.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": found_entries
        })

def newentry(request):
    """renders a new entry form page"""
    return render(request, "encyclopedia/newentry.html")

def saveentry(request):
    """Used to save a post in the local storage when save entry button is clicked"""
    title = request.POST.get("t", "")
    content = request.POST.get("content","")
    #check if the articles with same name already exists
    if title.lower() in [entry.lower() for entry in util.list_entries()]:
        return HttpResponse("Cannot save page. Page already exists")
    #create new file with name as the title of the page
    with open(f"entries/{title}.md", "w") as file:
        file.write(content)
    return redirect("wiki:pages", title)

def editpage(request):
    """Used to edit the existing webpage"""
    #fetch the title of the page to open file
    title = request.POST.get("title", "")
    with open(f"entries/{title}.md", "r") as readfile:
        content = readfile.read()
    
    return render(request, "encyclopedia/editpage.html", {"content": content, "title": title})

def savechanges(request):
    """Save the changes made to the webpage"""
    #get title from the webpage
    title = request.POST.get("title", "")
    #get updated from the page
    content = request.POST.get("editedContent", "")
    #save the webpage in local storage
    util.save_entry(title, content)
    return redirect("wiki:pages", title)
    
def randompage(request):
    #select a random page
    title = random.choice(util.list_entries())
    return redirect("wiki:pages", title)

def delete(request):
    """Delete an existing page"""
    #get title from the webpage
    title = request.POST.get("title", "")
    #if the file exist in entries delete that file
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    return HttpResponseRedirect(reverse("wiki:index"))