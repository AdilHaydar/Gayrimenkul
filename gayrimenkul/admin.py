from django.contrib import admin
from .models import Post, PostImage
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['seller','title','mkare','price','il','ilce','mahalle']
    list_display_links = ['seller','title']
    search_fields = ['seller','title']
    list_filter = ['il','ilce','mahalle']

    class Meta:
        model = Post


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):

    list_display = ['post']
    list_display_links = ['post']
    search_fields = ['post']

    class Meta:
        model = PostImage