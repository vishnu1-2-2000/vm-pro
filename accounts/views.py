from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View,ListView,CreateView,DetailView,UpdateView,DeleteView,FormView,TemplateView
from accounts.forms import Loginform
# from .models import Bikes,Bikeprofile,BikeApplication
from django.urls import reverse_lazy
# from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from accounts.models import Register,UserrolePermissions,Loginmodel
from django.contrib import messages
import json
# Create your views here.
class Homeview(View):
      def get(self,request):
        return render(request,"home.html")


class Signinview(FormView):
    form_class = Loginform
    template_name = "login.html"
    def post(self,request,*args,**kwargs):
        form=Loginform(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
          
            
            # print(userrole)
            userData=Register.objects.filter(email=uname).values()
            ud=Register.objects.get(email=uname)
            # print(ud.userRole)
            
            if userData:
#                 if(userData[0]['password']== pwd):

                   userData1=""
                   userData1=Register.objects.filter(password=pwd).values()
                #    pd=Register.objects.get(password=pwd)
                #    print(pd.userRole)
                   
                  
                #    for ele in userData1:
                #         print(ele['userRole'])                   
                                            
                #    userData2=UserrolePermissions.objects.filter(activity_name="printerjobs").values()
                   if  userData1:
                            ud=Register.objects.get(email=uname)
                            print(ud.userRole)
                            ghname=ud.Name
                            bt=ud.userRole
                            # login(request,ud)
                           
                            perm=UserrolePermissions.objects.filter(activity_name="printerjobs").values()
                            if bt=="admin":
                                if(perm[0]['admin']['READ']=="Checked"):
                                    return  redirect("web-home")
                                    # return render(request, 'home.html', {'sd':ghname,})
                                else:
                                     return HttpResponse ("Permission Denied!!!")                    
                            elif bt=="operator":
                                # print(perm[0]['operator']['READ'])
                                if(perm[0]['operator']['READ']=="Checked"):
                                    # return  redirect("web-home")
                                    return render(request, 'scannersoftware.html', {'sd':ud.Name})
                                else:
                                     return HttpResponse ("Permission Denied!!!")  
                            elif bt=="supervisor":
                                                    # print(perm[0]['operator']['READ'])
                                if(perm[0]['supervisor']['READ']=="Checked"):
                                    return  redirect("web-home")
                                else:
                                     return HttpResponse ("Permission Denied!!!")
                            elif bt=="masterdata":
                                                    # print(perm[0]['operator']['READ'])
                                if(perm[0]['masterdata']['READ']=="Checked"):
                                    return  redirect("web-home")
                                else:
                                     return HttpResponse ("Permission Denied!!!")                            
                   else:
                      return HttpResponse ("Password is incorrect!!!")
            else:
                  return HttpResponse ("User does not exit")
           
        
        else:
          return render(request, 'login.html' )
      
#             user=authenticate(request,username=uname,password=pwd)
#             if user:
#                 login(request,user)
#                 if request.user.userRole=="admin":
#                     return redirect("web-home")
#                 elif request.user.userRole=="manager":
#                     return  redirect("web-home")
#                 elif request.user.userRole=="operator":
#                     return  redirect("web-home")
#             else:
#                 return render(request,"login.html",{"form":form})
# ................................................................................

# webapplication login page code



def signout_view(request,*args,**kwargs):
        logout(request)
        return redirect("signin")


                                      
