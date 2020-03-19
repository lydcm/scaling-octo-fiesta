from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

def show_page(request):
    return render(request, "login.html")

# Register New User

def register_new_user(request):
    errors = UserInfo.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        new_user = UserInfo.objects.create(first_name = request.POST["first_name"], last_name = request.POST["last_name"], email = request.POST["email"], pw_hash = hash1)
        request.session["userid"] = new_user.id
        messages.success(request, "You are successfully registered!")
        return redirect("/success")

# Login User

def login_user(request):
    # check if email's matched 
    try:
        UserInfo.objects.get(email = request.POST["email"])
    except:
        messages.error(request, "User does not exist. Please register!")
        return redirect("/")
    logged_user = UserInfo.objects.get(email = request.POST["email"])
    if bcrypt.checkpw(request.POST["password"].encode(), logged_user.pw_hash.encode()):
        request.session["userid"] = logged_user.id
        messages.success(request, "You're successfully logged in!!")
        return redirect("/success")
    else:
        messages.error(request, "Incorrect password!")
        return redirect("/")      
        
    
# Go to "Success/Welcome" page

def success(request):
    if not "userid" in request.session:
        messages.error(request, "You're not logged in!")
        return redirect("/")
    else:
        user_info = UserInfo.objects.get(id=request.session["userid"])
        context = {
            "my_user_info" : user_info
        }
        return render(request, "success.html", context)    

# Logout User

def logout_user(request):
    request.session.clear()
    return redirect("/")
