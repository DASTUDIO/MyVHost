# coding=utf-8
from django.http import HttpResponse as show_text
from django.contrib.auth import authenticate
from django.contrib.auth import login as sys_login
from django.contrib.auth.models import User
import pub.functions.forms as forms

import pub.models as db

#from django.views.decorators.csrf import csrf_protect



def login(request):

    if request.method != 'POST':
        return show_text('-1')

    form = forms.reg(request.POST)
    
    if not form.is_valid():
        return show_text('-1')

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    user = authenticate(request,username=username,password=password)

    if user is not None:
        sys_login(request,user)
        return show_text('1')
    else:
        return show_text('0')



def register(request):
    if request.method != 'POST':
        return show_text('-1 not post')

    form = forms.reg(request.POST)
    if not form.is_valid():
        return show_text('-1 form not valid')

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    phone = form.cleaned_data['phone']
   # verify = form.cleaned_data['verify']



    #try:
    user = User.objects.create_user(username=username,password=password)
    user.save()

    user_detail = db.user_detail.objects.create(username=username,phone_number=phone)

    user_detail.save()

    return show_text(user_detail.id)
    #except:
    #    return show_text('0')


#def gen_verification(phone_number):
    









