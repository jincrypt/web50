from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util
import re

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def pages(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/pages.html", {
            "title": title,
            "content": util.markdownToHTML(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/pages.html", {
            "title": "Error",
            "content": "<h1>Error</h1> <p>Page was not found.</p>"
        })


def search(request):
    try:
        searchQuery = request.GET["q"]
        if request.method == "GET" and util.get_entry(searchQuery) != None:
            return HttpResponseRedirect(reverse("pages", kwargs={'title': searchQuery}))
        else:
            searchResults = []
            for i in util.list_entries():
                result = re.match(f'^({searchQuery})', i, flags=re.IGNORECASE)
                if result:
                    searchResults.append(result.string)

            return render(request, "encyclopedia/search.html", {
                'searchResults': searchResults
            })

    except MultiValueDictKeyError:
        return HttpResponseRedirect('/')

class NewPageForm(forms.Form):
    pageTitle = forms.CharField(label="Title",
                                widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    pageContent = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mb-2'}),                                        
                                label="Content")

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['pageTitle']
            content = form.cleaned_data['pageContent']

            # If the entry already exists, return error alert
            if title in util.list_entries():
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "alert": f"Page with title '{title}' already exists."
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("pages", kwargs={'title': title}))

    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm()
    })

def edit_page(request, title):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            editTitle = form.cleaned_data['pageTitle']
            editContent = form.cleaned_data['pageContent']
            if title != editTitle:
                util.delete_entry(title)
            util.save_entry(editTitle, editContent)
            return HttpResponseRedirect(reverse("pages", kwargs={'title': editTitle}))

    elif request.method == "GET" and util.get_entry(title) != None:

        form = NewPageForm({'pageTitle': title, 'pageContent': util.get_entry(title)})
        return render(request, "encyclopedia/edit_page.html", {
            'form': form,
            'title': title
        })

    else:
        return render(request, "encyclopedia/edit_page.html", {
            "title": "Error",
            "content": "<h1>Error</h1> <p>Page was not found.</p>"
        })


def random_page(request):
    return HttpResponseRedirect(reverse("pages", kwargs={'title': util.random_entry()}))