from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('create',views.post_create,name="create"),
    path('detail/<str:slug>',views.post_detail,name="detail"),
    path('list',views.post_list,name="list"),
    path('update/<str:slug>',views.post_update,name="update"),
    path('delete/<str:slug>',views.post_delete,name="delete"),
]