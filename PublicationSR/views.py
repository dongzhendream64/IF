from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from PublicationSR.SPARQL_Query import get_content_list
from PublicationSR.recomment import film_recommend

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

def rec_view(req):
    pubname = req.GET.get('pubname')
    # 获取推荐信息
    recomment_info = film_recommend(pubname, 10)
    return render_to_response('RecommentAndView.html', {'pubreclist': recomment_info})