from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .forms import RegisterForm, LoginForm, UserUpdateForm
from .models import User
#from django.contrib.auth.models import User
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.views.generic import CreateView, FormView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random, string
import sqlite3
# Create your views here.

User = get_user_model()
def register(request):
    form = RegisterForm(request.POST or None)
    context = {
            "form" : form
        }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        full_name = form.cleaned_data.get("full_name")
        registration_code = form.cleaned_data.get("registration_code")
        cep_telefonu = form.cleaned_data.get("cep_telefonu")
        is_telefonu = form.cleaned_data.get("is_telefonu")
        con = sqlite3.connect("code.db")
        cursor = con.cursor()
        cursor.execute("Select * From r_code")
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == registration_code:
                registeredUser = User(username = username,cep_telefonu=cep_telefonu,is_telefonu=is_telefonu, email = email,full_name=full_name,registration_code = registration_code)
                registeredUser.set_password(password)
                registeredUser.save()
                login(request, registeredUser)
                cursor.execute("Delete From r_code Where Kod = ?", (registration_code,))
                con.commit()
                con.close()
                messages.success(request,"Başarılı Bir Şekilde Kayıt Oldunuz.")
                return redirect("index")
        else:
            messages.warning(request,"Girmiş olduğunuz Davet kodu geçerli değildir!","danger")
    return render(request,"register.html",context)
        
def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        "form" : form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.info(request,"User does not exist.")
            return render(request,"login.html",context)
        messages.success(request,"Giriş Başarılı")
        login(request,user)
        return redirect("index")
    return render(request,"login.html",context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Güvenli Bir Şekilde Çıkış Yaptınız")
    return redirect("index")




@login_required(login_url = "index")
def userPanel(request,username):
    userInfo = User.objects.get(username=username)
    if request.user.username == username or request.user.is_admin:
        if request.method == "POST":
            userInfo.is_telefonu = request.POST.get("is_telefonu")
            userInfo.cep_telefonu = request.POST.get("cep_telefonu")
            userInfo.email = request.POST.get("email")
            userInfo.full_name = request.POST.get("full_name")
            if request.POST.get("password") == request.POST.get("confirm"):
                password = request.POST.get("password")
                userInfo.set_password(password)
            else:
                messages.warning(request,"Parolalar Uyuşmuyor","danger")
                return render(request,"userPanel.html",{"userInfo":userInfo,'username':username})
            userInfo.save()
            messages.success(request,"Kullanıcı Bilgileriniz Güncellenmiştir.")
            return redirect("index")
        return render(request,"userPanel.html",{"userInfo":userInfo,'username':username})
    else:
        messages.warning(request,"Bu sayfayı görüntüleyemezsiniz !!!","danger")
        return redirect("index")

def get_random_alphaNumeric_string(stringLength=30):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))
     
@login_required(login_url = "index")
def CreateRegistrationCode(request):
    if request.user.is_admin:
        con = sqlite3.connect("code.db")
        cursor = con.cursor()
        cursor.execute("Create Table If Not Exists r_code (Kod TEXT unique, isActive Boolean)")
        cursor.execute("Select * From r_code")
        rows = cursor.fetchall()
        context = {
            "rows":rows,
        }
        if request.method == "POST":
            key = get_random_alphaNumeric_string()
            
            for row in rows:
                if key == row[0]:
                    messages.warning(request,"Kod Oluşturulurken Hata Oluştu Lütfen Tekrar Deneyiniz.","danger")
                    return redirect("/user/code")
            cursor.execute("INSERT INTO r_code Values(?,?);", (key,False))
            con.commit()
            con.close()
            messages.success(request,"Davet Kodu Başarıyla Oluşturuldu. Kod : "+key)
            return redirect("/user/code")
        return render(request,"r_code.html",context)
    messages.warning(request,"Bu sayfayı görüntüleme yetkiniz yok. Ana sayfaya yönlendirildiniz.","danger")
    return redirect("index")

        
