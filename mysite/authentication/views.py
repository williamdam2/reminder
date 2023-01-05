from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from .lg_auth import *

def login_form(request):
    if request.user.is_authenticated:
        return redirect('reminder')
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('pass')
        # print(user)
        # print(password)
        user = authenticate(request, username = user , password = password )
        if user is not None:
            login(request, user)
            if('next' in request.GET):
                return redirect(request.GET.get('next'))
            else:
                return redirect('reminder')
        else:
            context = {'title':"Login",'loginfail':"User, Password or both are wrong!"}
            return render(request,"authentication/login.html",context)
    else:
        context = {'title':"Login"}
        return render(request,"authentication/login.html",context)

def logout_form(request):
    logout(request)
    context = {'title':"Logout"}
    return render(request,"authentication/logout.html",context)

def register_form(request):
    context = {'title':"Register"}  
    if request.user.is_authenticated:
        base_url = reverse('logout_form')
        next = reverse('register_form')
        delay = 5000
        url = '{}?next={}&delay={}'.format(base_url,next,delay)
        return redirect(url)
    else:
        gportal_template = "authentication/gportal.html"
        register_template = "authentication/register.html"
        the_template =""
        if request.method == "POST":
            user = request.POST.get('user')
            print(user)
            gpass = request.POST.get('gpass')
            password = request.POST.get('pass')
            re_password = request.POST.get('re_pass')
            verification = request.POST.get('verification')
            displayName = request.POST.get('displayName')
            print(displayName)
            email = request.POST.get('email')
            department = request.POST.get('department')
            if(verification=="1"): #check gportal user
                if(auth_ldap(user,gpass)):
                    user_profile = get_user_profile(user,gpass)
                    department = user_profile["entries"][0]["attributes"]["department"]
                    displayName = user_profile["entries"][0]["attributes"]["displayName"]
                    email = user_profile["entries"][0]["attributes"]["mail"]
                    context.update({'user':user,'gpass':gpass,'department':department,'displayName':displayName,'email':email})
                    the_template = register_template 
                else:
                    the_template = gportal_template
                    context.update({'register_fail':"Your Gportal User or Password is wrong"})
            if(verification=="2"):  
                print("========================check========================")
                if(User.objects.filter(username = user).exists()):
                    print("========================1========================")
                    context.update({'register_fail':"This User has already registered!"})
                elif(re_password==None or password==None):
                    print("========================2========================")
                    context.update({'register_fail':"Some fields is missing!"})
                elif(re_password!=password):
                    print("========================3========================")
                    context.update({'register_fail':"Password and Re-type is not matching!"})
                elif(auth_ldap(user,gpass)==False):
                    print("========================4========================")
                    print(user)
                    print(gpass)
                    context.update({'register_fail':"Gportal verification level 2 is fails"})
                    the_template = gportal_template
                    return render(request,the_template,context)
                else:
                    print("========================5========================")
                    print(user)
                    print(password)
                    print(displayName)
                    print(department)
                    print(email)
                    register_user = User.objects.create_user(email=email,username=user,password=password)
                    register_user.first_name = displayName
                    register_user.save()
                    user = authenticate(request, username = user , password = password )
                    login(request,user)
                    context.update({'register_ok':"Sign-ups were successful!"})
                context.update({'user':user,'gpass':gpass,'department':department,'displayName':displayName,'email':email})    
                the_template = register_template
                
            
        elif request.method == "GET":
            the_template = gportal_template
        return render(request,the_template,context)
# Create your views here.
