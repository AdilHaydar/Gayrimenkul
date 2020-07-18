from django.contrib import admin
from django.urls import path
from . import views
#from .views import RegisterView
app_name = "user"


urlpatterns = [
    path('login/',views.loginUser,name = "login"),
    path('register/',views.register,name = "register"),
    path('logout/',views.logoutUser,name = "logout"),
    path('panel/<str:username>',views.userPanel,name="userPanel"),
    path('code/',views.CreateRegistrationCode,name="code"),
]