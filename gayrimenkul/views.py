from django.shortcuts import render,HttpResponse,redirect,reverse,HttpResponseRedirect,Http404,get_object_or_404
from .models import Post, PostImage
from django.contrib import messages
from django.forms import modelformset_factory
from .forms import PostForm, PostImageForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import os
# Create your views here.


def index(request):

    return render(request,'carousel.html')

@login_required(login_url = "user:login")
def post_create(request):
    if not request.user.is_authenticated:
        raise Http404
    ImageFormSet = modelformset_factory(PostImage, form=PostImageForm, extra=5)
   
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=PostImage.objects.none())
        if post_form.is_valid():
            created_post = post_form.save(commit=False)
            created_post.seller = request.user
            created_post.save()
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = PostImage(post=created_post, image=image)
                    photo.save()
            messages.success(request,'Tebrikler, İlanınız Başarıyla Verildi.')
            return HttpResponseRedirect(reverse('gayrimenkul:detail',kwargs={'slug':created_post.get_slug()}))
    else:
        post_form = PostForm()
        formset = ImageFormSet(queryset = PostImage.objects.none())
    return render(request,'post_create.html',{'form':post_form,'formset':formset})

@login_required(login_url = "user:login")
def post_detail(request,slug):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise Http404
        if request.user == post.seller or request.user.is_admin:
            
            images = PostImage.objects.filter(post=post)
            for i in images:
                print(i.image)
            return render(request,'ilan_detay.html',{'post':post,'images':images})
        else:
            raise Http404

@login_required(login_url = "user:login")
def post_list(request):
    if request.user.is_authenticated:
        page = request.GET.get('page',1)
        if request.user.is_admin:
            posts = Post.objects.all()
        else:
            posts = Post.objects.filter(seller = request.user)
        paginator = Paginator(posts, 10)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request,'ilan_list.html',{'posts':posts})
    return redirect("index")

def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not request.user.is_authenticated and (not request.user == post.seller or not request.user.is_admin):
        raise Http404
    data = PostImage.objects.filter(post = post)
    ImageFormSet = modelformset_factory(PostImage, form=PostImageForm, extra=5, can_delete = True)
    form = PostForm(prefix='post',data=request.POST or None, instance = post, files = request.FILES or None)
    formset = ImageFormSet(data=request.POST or None, files= request.FILES or None, queryset=data)
    if form.is_valid():
        if formset.is_valid():
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        pic = PostImage(post=post, image=f.cleaned_data.get('image'))
                        pic.save()
                    elif request.POST.get('form-'+str(index)+'-DELETE') != None:
                        pic = PostImage.objects.get(id = request.POST.get('form-' + str(index) + '-id'))
                        pic.delete()
                    else:
                        pic = PostImage(post=post, image=f.cleaned_data.get('image'))
                        d = PostImage.objects.get(id=data[index].id)
                        d.image = pic.image
                        d.save()
        form.save(commit=True)
        messages.success(request,"İlanınız Başarıyla Güncellenmiştir")
        return HttpResponseRedirect(reverse('gayrimenkul:detail',kwargs={'slug':form.instance.slug}))
    return render(request,'post_update.html',{'form':form,'formset':formset,'slug':slug})

@login_required()
def post_delete(request,slug):
    if not request.user.is_authenticated:
        raise Http404
    post = get_object_or_404(Post,slug = slug)
    if request.method == "POST" and (request.user.is_admin or post.seller == request.user):
        post.delete()
        messages.warning(request,'İlan Silindi',"danger")
        return HttpResponseRedirect(reverse('gayrimenkul:list'))
    if request.method == "GET" and (request.user.is_admin or post.seller == request.user):
        post.delete()
        messages.warning(request,'İlan Silindi',"danger")
        return redirect('administrator:administrator')
    return HttpResponseRedirect(reverse('gayrimenkul:list'))
