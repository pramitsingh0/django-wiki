from django.shortcuts import render
import markdown2
from django import forms

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def pages(request, title):
    if title in util.list_entries():
        file = util.get_entry(title)
        htmlfile = markdown2.markdown(file)
        return render(request, "encyclopedia/pages.html", {
            "title": title,
            "body": htmlfile
        })


