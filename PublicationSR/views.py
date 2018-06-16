from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from PublicationSR.SPARQL_Query import get_content_list

# Create your views here.
class SearchForm(forms.Form):
    searchtxt = forms.CharField()

def search(req):
    searchtxt = {}
    return render_to_response('search.html', {'searchtxt': searchtxt})

def go_search(req):
    searchtxt = req.POST['searchtxt']
    search_result = get_content_list(searchtxt)
    return render_to_response('search.html', {'searchtxt': search_result})

def index(req):
    return render_to_response('index.html')