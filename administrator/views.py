from django.shortcuts import render,HttpResponse,redirect,reverse,HttpResponseRedirect,Http404,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.models import User
from gayrimenkul.models import Post
from .filters import PostFilter, UserFilter
import os
# Create your views here.

def administrator(request):
    if request.user.is_admin:
        page = request.GET.get('page',1)
        ilanlar = Post.objects.all()
        myFilter = PostFilter(request.GET, queryset=ilanlar)
        ilanlar = myFilter.qs
        paginator = Paginator(ilanlar, 10)
        try:
            ilanlar = paginator.page(page)
        except PageNotAnInteger:
            ilanlar = paginator.page(1)
        except EmptyPage:
            ilanlar = paginator.page(paginator.num_pages)
        return render(request,"admin.html",{"ilanlar":ilanlar,'myFilter':myFilter})
    return redirect("index")


def users(request):
    if request.user.is_admin:
        page = request.GET.get('page',1)
        kullanicilar = User.objects.all()
        myFilter = UserFilter(request.GET, queryset=kullanicilar)
        kullanicilar = myFilter.qs
        paginator = Paginator(kullanicilar,10)
        try:
            kullanicilar = paginator.page(page)
        except PageNotAnInteger:
            kullanicilar = paginator.page(1)
        except EmptyPage:
            kullanicilar = paginator.page(paginator.num_pages)
        return render(request,'adminPanelUser.html',{'kullanicilar':kullanicilar,'myFilter':myFilter})
    return redirect('index')

