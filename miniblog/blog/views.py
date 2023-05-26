from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Signup,loginform,Dataform
from django.contrib import messages
from .models import Data
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
# Create your views here.
#home
def home(request):
    post = Data.objects.all()
    return render(request,'blog/home.html',{'form':post})

#About
def about(request):
    return render(request,'blog/about.html')

#Contact page
def contact(request):
    return render(request,'blog/contact.html')

#Dash Board
def dashborad(reqeust):
    if reqeust.user.is_authenticated:
        form = Data.objects.all()
        return render(reqeust, 'blog/dashboard.html',{'forms':form})
    else:
        return HttpResponseRedirect('/login/')

#Sign Board
def user_signup(reqeust):
    if reqeust.method == 'POST':
        fm = Signup(reqeust.POST)
        if fm.is_valid():
            messages.success(reqeust,'Congratulations! You have been Signup successfully Signup')
            user = fm.save()
            group = Group.objects.get(name='writer')
            user.groups.add(group)
    else:
        fm = Signup()
    return render(reqeust, 'blog/signup.html',{'forms':fm})

#login Board
def user_login(reqeust):
    if not reqeust.user.is_authenticated:
        if reqeust.method =='POST':
            form = loginform(request=reqeust, data=reqeust.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username = uname ,password = upass)
                if user is not None:
                    login(reqeust, user)
                    messages.success(reqeust,'Congratulations ! You have been successfully login')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = loginform()
        return render(reqeust, 'blog/login.html',{'forms':form})
    else:
        return HttpResponseRedirect('/dashboard/')

#logout Board
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#add post
def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = Dataform(request.POST)
            if fm.is_valid():
                title = fm.cleaned_data['title']
                desc = fm.cleaned_data['desc']
                pst = Data(title = title, desc=desc)
                pst.save()
                fm = Dataform()
        else:
            fm = Dataform()
        return render(request,'blog/addpost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')
    
def updatepost(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Data.objects.get(pk=id)
            form = Dataform(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Data.objects.get(pk=id)
            form = Dataform(instance=pi)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
    

def deletepost(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Data.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')