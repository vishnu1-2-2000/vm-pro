from django.contrib import admin
from accounts import views
from django.urls import path
urlpatterns = [
  path("home",views.Homeview.as_view(),name="web-home"),
 
  path("users/accounts/signin",views.Signinview.as_view(),name="signin"),
  path("users/accounts/signout",views.signout_view,name="signout"),               
]