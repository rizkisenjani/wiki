from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django import forms

from . import util

class SearchForm(forms.Form):
    form = forms.CharField(label="", max_length=100)

class NewPage(forms.Form):
    title = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    text_area = forms.CharField(label="", max_length=1000, widget=forms.Textarea(attrs={'placeholder': 'Text here ...'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm(),
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": util.get_entry(title),
        "form": SearchForm(),
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["form"]
            return render(request, "encyclopedia/search.html", {
                "form": form,
                "title": query,
                "content": util.get_entry(query),
            })
    else:
        form = SearchForm()

    return render(request, "encyclopedia/search.html", {
        "form": form,
    })

def new_page(request):
    if request.method == "POST":
        new_page_form = NewPage(request.POST)
        if new_page_form.is_valid():
            entries = util.list_entries()
            title = new_page_form.cleaned_data['title']
            text = new_page_form.cleaned_data['text_area']
            if title in entries:
                return render(request, "encyclopedia/errors.html", {
                    "form": SearchForm(),
                    "error": f"A page with title '{title}' already exists."
                })
            else:
                new_entry = util.save_entry(title, text)
                content = util.get_entry(title)
                return render(request, "encyclopedia/entry.html", {
                    "form": SearchForm(),
                    "title": title,
                    "content": content,
                })
    return render(request, "encyclopedia/newpage.html", {
        "form": SearchForm(),
        "new_page_form": NewPage()
    })

def edit_page(request, title):
    content = util.get_entry(title)
    new_page_form = NewPage(initial={
        'title': title,
        'text_area': content,
        })
    if request.method == "POST":
        new_page_form = NewPage(request.POST, initial={
        'title': title,
        'text_area': content,
        })
        if new_page_form.is_valid():
            new_content = new_page_form.cleaned_data['text_area']
            util.save_entry(title, new_content)
            return render(request, "encyclopedia/entry.html", {
                "form": SearchForm(),
                "title": title,
                "content": new_content,
            })
    return render(request, "encyclopedia/editpage.html", {
        "new_page_form": new_page_form,
        "content": content,
        "title": title,
        "form": SearchForm(),
    })