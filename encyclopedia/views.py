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
    import markdown2
    content = util.get_entry(title)
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content,
        "form": SearchForm(),
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            query = form.cleaned_data["form"]
            query = query.lower()
            print(query)
            #for entry_item in entries:
                #if query in entry_item.lower():
            return render(request, "encyclopedia/search.html", {
                #"new_entry" : entry_item,
                "query": query,
                "entries": entries,
                "form": SearchForm(),
            })
                #else:
                    #pass
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
                return entry(request, title)
    return render(request, "encyclopedia/newpage.html", {
        "form": SearchForm(),
        "new_page_form": NewPage()
    })

def edit_page(request, title):
    text_area = util.get_entry(title)
    new_page_form = NewPage(initial={
        'title': title,
        'text_area': text_area,
        })
    if request.method == "POST":
        new_page_form = NewPage(request.POST)
        if new_page_form.is_valid():
            entries = util.list_entries()
            title = new_page_form.cleaned_data['title']
            text = new_page_form.cleaned_data['text_area']
            new_entry = util.save_entry(title, text)
            return entry(request, title)
    return render(request, "encyclopedia/editpage.html", {
        "new_page_form": new_page_form,
        "title": title,
        "form": SearchForm(),
    })

def random_page(request):
    entries = util.list_entries()
    import random
    random_title = random.choice(entries)
    return HttpResponseRedirect(f"/wiki/{random_title}")

