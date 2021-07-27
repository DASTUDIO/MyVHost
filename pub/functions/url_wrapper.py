# coding=utf-8
from django.shortcuts import render

def http_wrap(request,url):
    ctx = {}
    ctx['src'] = 'http://'+ url
    return render(request,'url_wrapper.html',ctx)

def https_wrap(request,url):
    ctx = {}
    ctx['src'] = 'https://' + url
    return render(request,'url_wrapper.html',ctx)


