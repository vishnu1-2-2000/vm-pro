from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View,ListView,CreateView,DetailView,UpdateView,DeleteView,FormView,TemplateView
from masterapp.forms import PrinterForm,CustomerForm,Dummyform,ScannerForm,Loginform
# from .models import Bikes,Bikeprofile,BikeApplication
from django.urls import reverse_lazy
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from masterapp.models import PrinterdataTable,Customers,ProductionOrder,ScannerTable
from django_filters.views import FilterView
from django.contrib import messages
from django_filters import FilterSet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import socket
import numpy as np
import json
import threading
import os
import webbrowser
import asyncio
import requests
import time
import subprocess
from queue import Queue
from multiprocessing import Event
from django.core.paginator import Paginator
from accounts.models import Register,UserrolePermissions,Loginmodel
# Create your views here.

class Autovisionopenview(View):
    def get(self,request,id):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""): 
            os.system('start D:\Omron\AutoVision\AutoVISION.exe') 
            qs=PrinterdataTable.objects.get(id=id)
            form=PrinterForm(request.POST,instance=qs)
            obj = PrinterdataTable.objects.get(id=id)
            detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(preparebuttonresponse=1)
            return  render(request,"scannersoftware.html",{"job":qs})
        else:
            return redirect("signin")
class Jobeditstopview(ListView):
    def get(self,request,id):
        qs=PrinterdataTable.objects.get(id=id)
        form=PrinterForm(instance=qs)
        return render(request,"cu-edit.html",{"form":form})

    def post(self,request,id):
        qs=PrinterdataTable.objects.get(id=id)
        form=PrinterForm(request.POST,instance=qs)
        if form.is_valid():                  
            form.save()
            return redirect("all-jobs") 
        else:
            return render(request,"cu-edit.html",{"form":form}) 
                        
def searchBar(request):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""): 
            if request.method == 'GET':
                query = request.GET.get('query')
                if query:
                    jobs = PrinterdataTable.objects.filter(gtin=query) 
                    return render(request, 'cu-list.html', {'page_obj':jobs,'search':1})
                else:
                    print("No information to show")
                    return render(request, 'cu-list.html', {})
        else:
            return redirect("signin")    
   
class listprinter(ListView):
    model = PrinterdataTable
    context_object_name = "jobs"
    template_name = "cu-list.html"

def listing(request) :
        hostname = socket.gethostname()
        systemip = socket.gethostbyname(hostname)
        # systemip="192.168.200.131"
        print(systemip)
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""):
            posts1 = PrinterdataTable.objects.all().filter(status="Running")
            if posts1:
                p = Paginator(posts1, 5)  
                page_num=request.GET.get('page',1)
                try:
                    page=p.page(page_num)
                except EmptyPage:
                    page=p.page(1)
           
                context = {'page_obj':page
                    }
                qs=PrinterdataTable.objects.get(status="Running")
                print(qs.responsefield)
                if qs.batchstopmessage==1:
                    return redirect("batch-stop-message")                   
                else:
                       
                    return render(request, 'cu-list.html', context)  
            else:
                posts = PrinterdataTable.objects.all().filter(ip_address=systemip)                        
                p = Paginator(posts, 5)  # creating a paginator object
                page_num=request.GET.get('page',1)
                try:
                    page=p.page(page_num)
                except EmptyPage:
                    page=p.page(1)
                context = {'page_obj':page
                        }            
                return render(request, 'cu-list.html', context)
        else:
            return redirect("signin")
    
class PauseClassview(View):
    pausestart=0
    qu=Queue()
    event=Event()
    def get(self,request,id):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        qs=PrinterdataTable.objects.get(id=id)
        if(loginname!="" ): 
            if(qs.responsefield==1): 
                qs=PrinterdataTable.objects.get(id=id)
                try:
                    serial=qs.numbers
                    serialno=json.loads(serial)
                except:
                    print("serialnumbers finished")    
                form=PrinterForm(request.POST,instance=qs)
                obj = PrinterdataTable.objects.get(id=id)
                detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(label_response=0,start_pause_btnresponse=0)
                
                print(obj.start_pause_btnresponse)
                try:
                    serilength=len(serialno)
                    print(serilength)
                except:
                    print("no length")
                    serilength=0
                
                return render(request,"pause-start.html",{"qs":qs,'lp':1,"sc":serilength,})
            else:
                return redirect("indexpage")
        else:
            return redirect("signin")
        
    def printerfun1(self,num,serialno,qu,event,gtin,lot,expire,hrfkey,hrfvalue,type,id):
        self.serialno=serialno
        self.gtin=gtin
        self.expire=expire
        self.lot=lot
        self.hrfkey=hrfkey
        self.hrfvalue=hrfvalue
        self.type=type  
        self.id=id
        print(hrfvalue)
        print(hrfkey)
        slle=len(serialno)                   
        s = socket.socket()
        port=34567
        s.connect(('192.168.200.150', port))
      
        
        obj = PrinterdataTable.objects.get(id=id)
        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(start_pause_btnresponse=1)
        # message51= "I6\x04"
        # # "I6\x04"
        # s.send(message51.encode()) 
        # data51=s.recv(1024).decode() 
        # dataex=int(data51[:-1])
        
        # message53= "K8\x04"
      
        # s.send(message53.encode()) 
        # data53=s.recv(1024).decode() 
        # data53ex=data53[:-1]
        # print(data52ex)
        # if(dataex==100):
        #      return redirect("printer-errors") 
        # message52= "K7\x04"
        # # "I6\x04"
        # s.send(message52.encode()) 
        # data52=s.recv(1024).decode() 
        # print(data52)
        
        
        # data51extract= data51[:-4]
        # print(data51)
        # if(data51>0):
        #     return redirect("printer-errors")               
       
        
        # detailsobj2 = PrinterdataTable.objects.get(id=id) 
        # prodObj=ProductionOrder.objects.get(gtin_number=detailsobj2.gtin)
        # detailObj3=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Running")
        # print(obj.start_pause_btnresponse)
        # else:
        # message100= "QAM,5\x04"
        # s.send(message100.encode()) 
        # data100=s.recv(1024).decode() 
        # print("data100"+data100) 
        if(type=="type2"):
                                    
                message= "L,new7.lbl\x04"
                s.send(message.encode()) 
                data=s.recv(1024).decode()  
                message1= "E\x04"        
                s.send(message1.encode()) 
                data1=s.recv(1024).decode()
                n=2
                d1=0
                a=0
                b=1 
                c=0
                d=5             
                upjso=[]                        
                while(n>0):
                            if(PauseClassview.qu.empty()):                                     
                                if d1==1:
                                        obj = PrinterdataTable.objects.get(id=id)
                                        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(loadpause=1)                    
                                                        
                                        for f in range(c,d):
                                            for sn in serialno[a:b]:              
                                                message5= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                                s.send(message5.encode()) 
                                                data5=s.recv(1024).decode()
                                            
                                                message6= "QAC\x09"  + "(01)" + gtin + "(21)" + sn + "(10)" + lot + "(17)" + expire + "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                                s.send(message6.encode()) 
                                                data6=s.recv(1024).decode() 
                                                                                
                                                message4= "F2\x04"
                                                s.send(message4.encode()) 
                                                data4=s.recv(1024).decode()
                                                
                                                a=a+1
                                                b=b+1   
                                            c=d
                                            d=d+5   
                            else:
                                d1=PauseClassview.qu.get()
                                if d1==0:
                                        a=0
                                        b=1 
                                        c=0
                                        d=5
                                        s8 = socket.socket()
                                        port8=34567
                                        s8.connect(('192.168.200.150', port8)) 
                                        obj = PrinterdataTable.objects.get(id=id)
                                        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(start_pause_btnresponse=0,label_response=1,loadpause=0)
                                        
                                        detailsObj = PrinterdataTable.objects.get(id=id) 
                                        prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
                                        detailObj=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Paused") 
                                        message32="QAF\x04"
                                        s8.send(message32.encode()) 
                                        data36=s8.recv(1024).decode()
                                        break
        elif(type=="type5"):
                        message7= "L,new8.lbl\x04"
                        s.send(message7.encode()) 
                        data7=s.recv(1024).decode() 
                         
                        message8= "E\x04"        
                        s.send(message8.encode()) 
                        data8=s.recv(1024).decode()
                        
                        detailsobj2 = PrinterdataTable.objects.get(id=id) 
                        prodObj=ProductionOrder.objects.get(gtin_number=detailsobj2.gtin)
                        detailObj3=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Running")            
                        n1=2
                        d1=0
                        a1=0
                        b1=1 
                        c1=0
                        d2=5             
                        upjso=[]                    
                        while (n1>0):
                                    if(PauseClassview.qu.empty()):                                   
                                        if d1==1:
                                                obj = PrinterdataTable.objects.get(id=id)
                                                detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(loadpause=1)                                    
                                                for f in range(c1,d2):
                                                    for sn in serialno[a1:b1]:              
                                                        message9= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x09"+"hrf"+"\x09hrfvalue"+"\x04"
                                                        s.send(message9.encode()) 
                                                        data9=s.recv(1024).decode()
                                                
                                                        message10= "QAC\x09"  + "(01)" + gtin + "(21)" + sn + "(10)" + lot + "(17)" + expire + "(45)" + hrfvalue + "\x09" + "Exp"+ "\x09" + expire + "\x09" + "Lot" + "\x09" + lot + "\x09" + "Gtin" + "\x09" +  gtin + "\x09" + "Slno" + "\x09" + sn + "\x09" + hrfkey + "\x09" + hrfvalue + "\x04"
                                                        s.send(message10.encode()) 
                                                        data10=s.recv(1024).decode() 
                                                                
                                                        message11= "F2\x04"
                                                        s.send(message11.encode()) 
                                                        data11=s.recv(1024).decode()
                                                
                                                        # print(a1)
                                                        # # serialno[a1:b1]
                                                        # upjso.append(serialno[a1:b1])
                                                        # jso=json.dumps(upjso)
                                                        # # print(jso)
                                                        
                                                        # obj = PrinterdataTable.objects.get(id=id)
                                                        # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(printed_numbers=jso)
                                                        
                                                        a1=a1+1
                                                        b1=b1+1
                                                        
                                                    c1=d2
                                                    d2=d2+5 
                                    else:
                                        d1=PauseClassview.qu.get()
                                        if d1==0:
                                                a1=0
                                                b1=1 
                                                c1=0
                                                d2=5
                                                s8 = socket.socket()
                                                port8=34567
                                                s8.connect(('192.168.200.150', port8))  
                                                obj = PrinterdataTable.objects.get(id=id)
                                                detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(start_pause_btnresponse=0,label_response=1,loadpause=0)
                                                
                                                detailsObj = PrinterdataTable.objects.get(id=id) 
                                                prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
                                                detailObj=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Paused")
                                                message32="QAF\x04"
                                                s8.send(message32.encode()) 
                                                data36=s8.recv(1024).decode()
                                                break
        elif(type=="type1"):
                        message12= "L,new5.lbl\x04"
                        s.send(message12.encode()) 
                        data12=s.recv(1024).decode()
                          
                        message13= "E\x04"        
                        s.send(message13.encode()) 
                        data13=s.recv(1024).decode()
                        n2=2
                        d1=0
                        a2=0
                        b2=1 
                        c2=0
                        d3=5                                 
                        while (n2>0):
                                    if(PauseClassview.qu.empty()):                                    
                                        if d1==1:
                                                obj = PrinterdataTable.objects.get(id=id)
                                                detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(loadpause=1)                                    
                                                for f in range(c2,d3):
                                                    for sn in serialno[a2:b2]:              
                                                        message14= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                                        s.send(message14.encode()) 
                                                        data14=s.recv(1024).decode()
                                                        
                                                                # print(slno)                    
                                                                # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                                        message15= "QAC\x09"  + "(01)" + gtin + "(21)" + sn + "(10)" + lot + "(17)" + expire + "(45)" + hrfvalue + "\x09" + "Exp\x09" + expire + "\x09" + "Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                                        # message15= "QAC\x09" + "(01)" +  gtin +  "(10)" + lot + "(17)" + expire +  "(21)" + sn +"(45)"+ hrfvalue +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                                        s.send(message15.encode()) 
                                                        data15=s.recv(1024).decode() 
                                                                        
                                                        message16= "F2\x04"
                                                        s.send(message16.encode()) 
                                                        data16=s.recv(1024).decode()
                                                            
                                                        a2=a2+1
                                                        b2=b2+1
                                                        
                                                    c2=d3
                                                    d3=d3+5      
                                    else:
                                        d1=PauseClassview.qu.get()
                                        if d1==0:
                                                a2=0
                                                b2=1 
                                                c2=0
                                                d3=5
                                                s8 = socket.socket()
                                                port8=34567
                                                s8.connect(('192.168.200.150', port8)) 
                                                obj = PrinterdataTable.objects.get(id=id)
                                                detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(start_pause_btnresponse=0,label_response=1,loadpause=0)
                                                
                                                detailsObj = PrinterdataTable.objects.get(id=id) 
                                                prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
                                                detailObj=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Paused")
                                                message32="QAF\x04"
                                                s8.send(message32.encode()) 
                                                data36=s8.recv(1024).decode()
                                                break
                                            
    def scannerfun1(self,num,serialno,qu,event):
        self.serialno=serialno                  
        counter=0
        d=0
        n=1
        s1 = socket.socket()
        port1=2001
        s1.connect(('192.168.200.134', port1))
        
        s = socket.socket()
        port=34567
        s.connect(('192.168.200.150', port))
        while True: 
            if(PauseClassview.qu.empty()):
                if d==1:
                    data=s1.recv(1024).decode() 
                    print(serialno[counter]) 
                    counter=counter+1    
                time.sleep(1)    
            else:
                d=PauseClassview.qu.get()
                if d==0:         
                    break
                time.sleep(1)  
    def post(self,request,id):
        qs=PrinterdataTable.objects.get(id=id)
        form=PrinterForm(request.POST,instance=qs) 
        gtin=qs.gtin 
        ponumber=qs.processordernumber
        expire =str(qs.expiration_date)
        lot=qs.lot 
        type=qs.type
        hrf=qs.hrf                            
        hrfjson=json.loads(hrf)
        hrf1value=hrfjson["hrf1value"]
        hrf1key=hrfjson["hrf1"]
        hrf2value=hrfjson["hrf2value"]
        hrf2key=hrfjson["hrf2"]  
        hrf3value=hrfjson["hrf3value"]
        hrf3key=hrfjson["hrf3"]        
        hrf4value=hrfjson["hrf4value"]
        hrf4key=hrfjson["hrf4"]
        hrf5key=hrfjson["hrf5"]
        hrf5value=hrfjson["hrf5value"]
        hrf6key=hrfjson["hrf6"]
        hrf6value=hrfjson["hrf6value"]     
        if(hrf1value!=""):
            hrfvalue=hrf1value             
        elif(hrf2value!=""):
            hrfvalue=hrf2value
        elif(hrf3value!=""):
            hrfvalue=hrf3value
        elif(hrf4value!=""):
            hrfvalue=hrf4value
        elif(hrf5value!=""):
            hrfvalue=hrf5value
        elif(hrf6value!=""):
            hrfvalue=hrf6value 
        print(hrfvalue)    
        if(hrf1key!="" and hrf1key!="null"):
            hrfkey=hrf1key      
        elif(hrf2key!="" and hrf2key!="null"):
            hrfkey=hrf2key
        elif(hrf3key!="" and hrf3key!="null"):
            hrfkey=hrf3key
        elif(hrf4key!="" and hrf4key!="null"):
            hrfkey=hrf4key
        elif(hrf5key!="" and  hrf5key!="null"):
            hrfkey=hrf5key
        elif(hrf6key!="" and hrf6key!="null"):
            hrfkey=hrf6key 
        try:
            serial=qs.numbers
            serialno=json.loads(serial)
            serialnum=qs.numbers
            serilength=len(serialno)
            print(serilength)
        except:
            print("pause printing because serialnumber are empty")
            serilength=0 
            serialno=[]   
        s = socket.socket()
        port=34567
        s.connect(('192.168.200.150', port))
        
        message51= "I6\x04"
        # "I6\x04"
        s.send(message51.encode()) 
        data51=s.recv(1024).decode() 
        dataex=int(data51[:-1])  
        print("ink")   
        print(dataex)     
        message53= "K8\x04"
        s.send(message53.encode()) 
        data53=s.recv(1024).decode() 
        data53ex=data53[:-1]                    
        if(PauseClassview.pausestart==0):                     
            PauseClassview.pausestart=1 
            PauseClassview.qu.put(PauseClassview.pausestart)
            # print(PauseClassview.pausestart)
            x1 = threading.Thread(target=PauseClassview.printerfun1,args=(self,10,serialno, PauseClassview.qu, PauseClassview.event,gtin,lot,expire,hrfkey,hrfvalue,type,id,))
            # y1.start()
            # print("hi")
            x1.start()
            # return redirect("{%url 'Process-start' qs.id %}")
           
            # return render(request, 'pause-start.html', {'qs': qs,'pd':1,"sc":serilength,"prer":dataex,"warningmess":data53ex})
            
            
        
           
        elif(PauseClassview.pausestart==1):
            PauseClassview.pausestart=0                    
            PauseClassview.qu.put(PauseClassview.pausestart)
            # return render(request, 'pause-start.html', {'qs': qs,'pd':0,"sc":serilength,"prer":dataex,"warningmess":data53ex})
            # print(PauseClassview.pausestart)
            # return redirect("process-paused")
            
            
            
            
        return render(request, 'pause-start.html', {'qs': qs,'pd':1,"sc":serilength,"prer":dataex,"warningmess":data53ex})
         
    def get_queryset(self):
        return PrinterdataTable.objects.all()              
 
class Viewprinterview(View):
    threadstart=0
    pausestart=0
    
    q=Queue()
    event=Event()
    
    def get(self,request,id):
            uname = Loginmodel.objects.get(id=2)
            loginname=uname.loginuname
            qs=PrinterdataTable.objects.get(id=id)
            if(loginname!=""):   
                
                if(qs.loadpause==0): 
                          
                    qs=PrinterdataTable.objects.get(id=id)
                    form=PrinterForm(request.POST,instance=qs)
                    return render(request,"cu-edit.html",{"qs":qs})
                else:
                     return redirect("httpalert1")
            else:
                return redirect("signin")
    def printerfun(self,num,serialno,q,event,gtin,lot,expire,hrfkey,hrfvalue,type,id):
        self.serialno=serialno
        self.gtin=gtin
        self.expire=expire
        self.lot=lot
        self.hrfkey=hrfkey
        self.hrfvalue=hrfvalue
        self.type=type 
        self.id=id
                    
        s2 = socket.socket()
        port2=34567
        s2.connect(('192.168.200.150', port2))

        if(type=="type2"):
                                
                    message= "L,new7.lbl\x04"
                    s2.send(message.encode()) 
                    data=s2.recv(1024).decode()  
                    message1= "E\x04"        
                    s2.send(message1.encode()) 
                    data1=s2.recv(1024).decode()
                    uy1=serialno[0:1]
                    
                    for sn in uy1:                
                 
                                   message5= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   s2.send(message5.encode()) 
                                   data5=s2.recv(1024).decode()
                                                
                                   message6= "QAC\x09" + "(17)"+expire+"(10)" + lot + "(01)" +  gtin + "(21)" + sn +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   s2.send(message6.encode()) 
                                   data6=s2.recv(1024).decode() 
                                          
                                   message4= "F2\x04"
                                   s2.send(message4.encode()) 
                                   data4=s2.recv(1024).decode()
                     
                    print('Received from server: ' + data5)
                    print('Received from server: ' + data6)         
                    print('Received from server: ' + data4)
           
        elif(type=="type5"):
                     message7= "L,new8.lbl\x04"
                     s2.send(message7.encode()) 
                     data7=s2.recv(1024).decode()  
                     
                     message8= "E\x04"        
                     s2.send(message8.encode()) 
                     data8=s2.recv(1024).decode()
                     
                     uy2=serialno[0:1]     
                     for sn in uy2: 
                        message9= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x09"+"hrf"+"\x09hrfvalue"+"\x04"
                        s2.send(message9.encode()) 
                        data9=s2.recv(1024).decode()
                                                   
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                        message10= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn + "(45)"+ hrfvalue+ "\x09" + "Exp\x09" + expire + "\x09"+"Lot" + "\x09" + lot + "\x09" + "Gtin"+ "\x09" +  gtin + "\x09" + "Slno" + "\x09" + sn + "\x09" + hrfkey + "\x09" + hrfvalue + "\x04"
                        s2.send(message10.encode()) 
                        data10=s2.recv(1024).decode() 
                                          
                        message11= "F2\x04"
                        s2.send(message11.encode()) 
                        data11=s2.recv(1024).decode()
                                        
                     print('Received from server: ' + data7)
                     print('Received from server: ' + data8) 
                     print('Received from server: ' + data9)
                     print('Received from server: ' + data10)         
                     print('Received from server: ' + data11)
                  
        elif(type=="type1"):
                     message12= "L,new5.lbl\x04"
                     s2.send(message12.encode()) 
                     data12=s2.recv(1024).decode()  
                     
                     message13= "E\x04"        
                     s2.send(message13.encode()) 
                     data13=s2.recv(1024).decode()
                     
                     uy=serialno[0:1] 
                                   
                     for sn in uy:
                                   message14= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   s2.send(message14.encode()) 
                                   data14=s2.recv(1024).decode()
                                                  
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                   message15= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn +"(45)"+ hrfvalue +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   s2.send(message15.encode()) 
                                   data15=s2.recv(1024).decode() 
                                          
                                   message16= "F2\x04"
                                   s2.send(message16.encode()) 
                                   data16=s2.recv(1024).decode()
       
                     print('Received from server: ' + data14)
                     print('Received from server: ' + data15)         
                     print('Received from server: ' + data16)

    def scannerfun(self,num,id,gtin,serialno,sl,printednumbers,q,event,lot,expire,hrfkey,hrfvalue,ip_address,child_numbers,type):
        self.id=id                    
        self.serialno=serialno
        self.sl=sl
        self.printednumbers=printednumbers
        self.gtin=gtin
        self.lot=lot
        self.expire=expire
        self.hrfkey=hrfkey
        self.hrfvalue=hrfvalue
        self.ip_address=ip_address
        self.child_numbers=child_numbers 
        self.type= type                
        counter=0
        d=0
        co=-1
        n=1
        s3 = socket.socket()
        port4=2001
        s3.connect(('192.168.200.134', port4))  #connecting the scanner to 2001 port 
        s3.settimeout(5)      #for timeouting the socket...break is working by using this
        s4 = socket.socket()
        port=34567
        s4.connect(('192.168.200.150', port))   #connecting the printer to 34567 port
        
        obj = PrinterdataTable.objects.get(id=id)
        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin)
        print(obj.printed_numbers)
        
        sllen=len(sl)
        print("sllen count")
        print(sllen)
        upjso=[]
        cd=0
        drg=[] 
        while True: 
                if(Viewprinterview.q.empty()):
                    try:       
                        data=s3.recv(1024).decode()
                        print(data)
                        print(type)
                        if(type=="type2"):
                            v=data[0] 
                            confidence=data[1] 
                            textbatch=data[11:25]
                            meanconfidence=data[2:7]
                            print(textbatch) 
                            print(meanconfidence)
                        elif(type== "type1" or type== "type5"):
                            v=data[0]
                            confidence=data[1]
                            textbatch=data[9:23]
                            meanconfidence=data[2:7]
                            print(textbatch)  
                            print(meanconfidence)                                     
                        if d==1:
                            try:
                                upjso.append(sl[counter])
                            except:
                                print("No serialnumbers available for printing")   
                            serilength=len(serialno)
                            try:
                                if(v=="4" and confidence=="1" and meanconfidence>="0.800"):
                                            grade="A"
                                elif(v=="3" and confidence=="1" and meanconfidence>="0.800"):
                                            grade="B"
                                elif (v=="2" and confidence=="1" and meanconfidence>="0.800"):
                                            grade="C"
                                elif (v=="1" and confidence=="1" and meanconfidence>="0.800"):
                                            grade="D"
                                else:
                                            grade="F" 
                                # if(v=="4" ):
                                #             grade="A"
                                # elif(v=="3" ):
                                #             grade="B"
                                # elif (v=="2" ):
                                #             grade="C"
                                # elif (v=="1" ):
                                #             grade="D"
                                # else:
                                #             grade="F" 
                                            
                                r={"serialnumber":sl[counter],
                                            "grade":grade}
                                
                                if(gtin==textbatch):
                                    if(v=="3" or v=="2"):                
                                        print(r)
                                        b=json.dumps(r)
                                        gradeupdation=ScannerTable(
                                        gtin=gtin,
                                        ip_address=ip_address,
                                        grade=b,
                                        status="NO"
                                        )
                                        gradeupdation.save()
                                        obj = PrinterdataTable.objects.get(id=id)
                                        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(scannergradefield=b)
                                        jso=json.dumps(upjso)
                                        serialno.remove(sl[counter])
                                        gh=json.dumps(serialno)
                                        print(sl[counter])
                                        obj = PrinterdataTable.objects.get(id=id)
                                        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(printed_numbers=jso,numbers=gh)
                                        updatedjson=json.loads(jso)
                                        if(counter==sllen-1):           #If the last number is detecting it will clear the serialno
                                            print(serialno)                    
                                            del serialno[:]
                                            obj = PrinterdataTable.objects.get(id=id)
                                            detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(numbers=serialno)                  
                                            print("detecte serialnumber cleared")     
                                        counter=counter+1
                                    else:    
                                        print("grade less then B")
                                else:                   
                                    print("not equal")
                                    r={"serialnumber":sl[counter],
                                            "grade":"Not Detected"}
                                    print(r)
                                    b=json.dumps(r)
                                    gradeupdation=ScannerTable(
                                    gtin=gtin,
                                    ip_address=ip_address,
                                    numbers=b,
                                    status="NO"
                                    )
                                    gradeupdation.save()
                                    obj = PrinterdataTable.objects.get(id=id)
                                    detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(scannergradefield=b)
                                    jso=json.dumps(upjso)
                                    serialvar=sl[counter]
                                    serialno.remove(sl[counter])
                                    serialno.append(serialvar)
                                    drg.append(serialvar)
                                    drgjson=json.dumps(drg)
                                    gh=json.dumps(serialno)
                                    obj = PrinterdataTable.objects.get(id=id)
                                    detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(numbers=gh,child_numbers=drgjson)
                                    if(counter==sllen-1):     #if the last number is not detecting it will clear the serialno
                                        print(serialno)                    
                                        del serialno[:]
                                        obj = PrinterdataTable.objects.get(id=id)
                                        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(numbers=serialno)
                                        print("not detecte serialnumber cleared")                  
                                    counter=counter+1
                            except:
                                print("serialnumbers finished")
                    except socket.timeout:
                        print("Didn't receive data! [Timeout 5s]")    
                else:
                        d=Viewprinterview.q.get()
                        print(d)
                        if d==0:
                                # if(gtin==textbatch):                
                                #     upjso.remove(sl[counter-1])
                                #     jso=json.dumps(upjso) 
                                #     serialno.insert(0,sl[counter-1]) 
                                #     # serialno.append(sl[counter-1])
                                #     gh=json.dumps(serialno)
                                #     print(serialno)
                                #     obj = PrinterdataTable.objects.get(id=id)
                                #     detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(printed_numbers=jso,numbers=gh) 
                                # else:        
                                print("Batch stop But Not update")
                                message30= "F0\x04"
                                s4.send(message30.encode()) 
                                data30=s4.recv(1024).decode()
                                if(serialno==[]):
                                    try:
                                        detailsObj = PrinterdataTable.objects.get(id=id)
                                        prodObj=PrinterdataTable.objects.get(gtin=detailsObj.gtin)
                                        no=prodObj.child_numbers
                                        # childnojson=json.loads(no)
                                        obj = PrinterdataTable.objects.get(id=id)
                                        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(balanced_serialnumbers=no)
                                        
                                        
                                    except:
                                        print("nochild numbers available")                          
                                    obj = PrinterdataTable.objects.get(id=id)
                                    detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(stopbtnresponse=1,return_slno_btn_response=0,status="Printed")
                                    
                                else:
                                    obj = PrinterdataTable.objects.get(id=id)
                                    detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(stopbtnresponse=1,return_slno_btn_response=0,status="Stopped")
                                        
                                detailsObj1 = PrinterdataTable.objects.get(id=id) 
                                prodObj=ProductionOrder.objects.get(gtin_number=detailsObj1.gtin)
                                detailObj2=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Closed")
                                        
                                obj = PrinterdataTable.objects.get(id=id)
                                detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(responsefield=0)                  
                                break                        
    def post(self,request,id):
        # global y  
        # self.running=True 
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""):                 
            qs=PrinterdataTable.objects.get(id=id)
            form=PrinterForm(request.POST,instance=qs)
            form2=PrinterForm(request.POST,instance=qs)
            id=qs.id    
            gtin=qs.gtin 
            ponumber=qs.processordernumber
            expire =str(qs.expiration_date)
            lot=qs.lot
            type=qs.type
            hrf=qs.hrf 
            printednumbers=qs.printed_numbers
            ip_address=qs.ip_address
            child_numbers=qs.child_numbers
            print(printednumbers) 
                                        
            hrfjson=json.loads(hrf) 
            hrf1value=hrfjson["hrf1value"]
            hrf1key=hrfjson["hrf1"]
            hrf2value=hrfjson["hrf2value"]
            hrf2key=hrfjson["hrf2"]
            hrf3value=hrfjson["hrf3value"]
            hrf3key=hrfjson["hrf3"]
            hrf4value=hrfjson["hrf4value"]
            hrf4key=hrfjson["hrf4"]
            hrf5key=hrfjson["hrf5"]
            hrf5value=hrfjson["hrf5value"]
            hrf6key=hrfjson["hrf6"]
            hrf6value=hrfjson["hrf6value"]
            
            if(hrf1key!="" or hrf1key!="null"):
                hrfkey=hrf1key
            elif(hrf2key!="" or hrf2key!="null"):
                hrfkey=hrf2key
            elif(hrf3key!="" or hrf3key!="null"):
                hrfkey=hrf3key
            elif(hrf4key!="" or hrf4key!="null"):
                hrfkey=hrf4key
            elif(hrf5key!="" or hrf5key!="null"):
                hrfkey=hrf5key
            elif(hrf6key!="" or hrf6key!="null"):
                hrfkey=hrf6key
            else:
                hrfkey="null"
            if(hrf1value!="" or hrf1value!="null"):
                hrfvalue=hrf1value
            elif(hrf2value!="" or hrf2value!="null"):
                hrfvalue=hrf2value
            elif(hrf3value!="" or hrf3value!="null"):
                hrfvalue=hrf3value
            elif(hrf4value!="" or hrf4value!="null"):
                hrfvalue=hrf4value
            elif(hrf5value!="" or hrf5value!="null"):
                hrfvalue=hrf5value
            elif(hrf6value!="" or hrf6value!="null"):
                hrfvalue=hrf6value
            else:
                hrfvalue="null"
            # print(hrfkey)
            # print(hrfvalue)
            try:    
                serial=qs.numbers
                serialnum=qs.numbers
                serialno=json.loads(serial)
                sl=json.loads(serialnum)
            except:
                print("No serialnumber available in viewprinterview")
                    
            # sk=len(sl)
            # print(sk)
            # print(serialno[0:10])
            # childjson= json.dumps(serialno[0:10])
            # obj = PrinterdataTable.objects.get(id=id)
            # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(child_numbers=childjson)
            # childserialnum=qs.child_numbers
            # print(childserialnum)
            # childsl=json.loads(childserialnum)
            # so1=json.dumps(serialno[11:13])
            # obj = PrinterdataTable.objects.get(id=id)
            # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(child_numbers=so1)
            try:
                s5 = socket.socket()
                port1=2001
                s5.connect(('192.168.200.134', port1))
            except:
                return redirect("scanner-message")
            try:
                s4 = socket.socket()
                port=34567
                s4.connect(('192.168.200.150', port))
                message52= "K7\x04"
                s4.send(message52.encode()) 
                data52=s4.recv(1024).decode() 
                data52ex=data52[:-1]
                if(Viewprinterview.threadstart==0):
                    if  TimeoutError:
                        messages.success(request,"your application has posted successfully")                                    
                    obj = PrinterdataTable.objects.get(id=id)
                    detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(responsefield=1,stopbtnresponse=0,return_slno_btn_response=1,batchstopmessage=0,status="Running")                     
                    Viewprinterview.threadstart=1
                    Viewprinterview.q.put(Viewprinterview.threadstart) 
                    # print(Viewprinterview.threadstart)
                    y = threading.Thread(target=self.scannerfun,args=(10,id,gtin,serialno,sl,printednumbers,Viewprinterview.q,Viewprinterview.event,lot,expire,hrfkey,hrfvalue,ip_address,child_numbers,type))
                    x = threading.Thread(target=self.printerfun,args=(10,serialno,Viewprinterview.q,Viewprinterview.event,gtin,lot,expire,hrfkey,hrfvalue,type,id))
                    y.start()
                    x.start()                       
                elif(Viewprinterview.threadstart==1):
                    Viewprinterview.threadstart=0                    
                    Viewprinterview.q.put(Viewprinterview.threadstart)
                    Viewprinterview.event.set()
                    obj = PrinterdataTable.objects.get(id=id)
                    detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(batchstopmessage=1)                     
                    return redirect("batch-stop-message")
                return render(request, 'cu-edit.html', {'sd':1,'qs': qs,'yu':0,'errormess':data52ex})
            except:
                print("An exception occurred")
                return redirect("cand-home")
        else:
            return redirect("signin")                   
class Candidatehomeview(TemplateView):
            template_name = "messagepage.html"           
class Scannermessageview(TemplateView):
        template_name = "Scannermessage.html"
class Batchstopmessageview(TemplateView):    
        template_name = "Batch-stop-message.html"                              
class Errorview(TemplateView):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""): 
            template_name = "printererror.html"        
class Scannersoftwareview(TemplateView):     
        template_name = "scannersoftware.html"
class HttpAlert1(TemplateView):     
        template_name = "Httpalert1.html" 
        
class ProcessStart(TemplateView):
        template_name = "Httpalert1.html"              
class Returnserialnumbers(View):
    def get(self,request,id):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""): 
            qs=PrinterdataTable.objects.get(id=id)
            form=PrinterForm(request.POST,instance=qs)
            y=[]
            y1=[]
            detailsObj = PrinterdataTable.objects.get(id=id)
            prodObj=PrinterdataTable.objects.get(gtin=detailsObj.gtin)
            serialno=prodObj.numbers
            if(serialno!=[]):
                detailObj2=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(balanced_serialnumbers=serialno,status="Printed")
                y.clear()
                obj = PrinterdataTable.objects.get(id=id)
                detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(numbers=y)   
            else:
                try:
                    child_number=prodObj.child_numbers
                    childnojson=json.loads(child_number)
                    # print(childnojson)    
                except:
                    print("no child_numbers")
                    childnojson=[] 
                y1.append(serialno+childnojson)
                y2 = list(np.concatenate(y1))
                print(y2)
                newjson=json.dumps(y2)
                obj = PrinterdataTable.objects.get(id=id)
                detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(balanced_serialnumbers=newjson,status="Printed")
                y2.clear()
                obj = PrinterdataTable.objects.get(id=id)
                detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(child_numbers=y2)      
            return render(request,"returnserial.html",{"qs":qs,"returnmessa":1})                              
        else:
            return redirect("signin")                       
class ReturnsnGet(View):
    def get(self,request,id):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""): 
            qs=PrinterdataTable.objects.get(id=id)
            form=PrinterForm(request.POST,instance=qs)
            return render(request,"returnserial.html",{"qs":qs})
        else:
            return redirect("signin")                                         
class Nextserialno(Viewprinterview):
    so1=[]                  
    def get(self,id):
        qs=PrinterdataTable.objects.get(id=id)
        serialno=qs.numbers
        serial=json.loads(serialno)
        print(serial[11:14])
        # form=PrinterForm(request.POST,instance=qs)
        so1=json.dumps(serial[11:14])
        print(so1)
        obj = PrinterdataTable.objects.get(id=id)
        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(child_numbers=so1)
        return so1
class Getgradedata(ListView):
   def get(self,request):
        qs=ScannerTable.objects.all().order_by('-id')
        p = Paginator(qs, 2)  # creating a paginator object
        page_num=request.GET.get('page',1) 
        try:
            page=p.page(page_num)
        except EmptyPage:
            page=p.page(1)
        # print(page)
        context = {'page_obj':  page,
                  }
        return render(request,"Grade.html",context)
    
class Gradecount(ListView):
    def get(self,request,id):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""):                    
            qs=PrinterdataTable.objects.get(id=id)
            try:
                val=qs.child_numbers
                serial=qs.numbers
                serialno=json.loads(serial)
                serialnum=qs.numbers
                serilength=len(serialno)
                print(val)
            except:
                print("no grade")
                serilength=0
            return render(request,"gradecount.html",{"qs":qs,"sc":serilength})       
        else:
            return redirect("signin")                      

class Serialnumberdownloadagainview(View):
    def get(self,request,id):              
        qs=PrinterdataTable.objects.get(id=id)
        # print(qs.numbers)
        jsonArray=[]
        jsonArray=json.loads(qs.numbers)
        print(qs.child_numbers)
        jlo=json.loads(qs.child_numbers)
        s2=json.dumps(jlo+jsonArray[0:10])
        obj = PrinterdataTable.objects.get(id=id)
        detailObj=PrinterdataTable.objects.filter(id=id).update(child_numbers=s2)
        del jsonArray[0:10]
        gh=json.dumps(jsonArray)
        obj = PrinterdataTable.objects.get(id=id)
        detailObj=PrinterdataTable.objects.filter(id=id).update(numbers=gh)
        return HttpResponse(200)

# WEBAPPLICATION LOGIN PAGE CODE

class Signinview(FormView):
    form_class = Loginform
    template_name = "login.html"
    def post(self,request,*args,**kwargs):
        form=Loginform(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            userData=Register.objects.filter(email=uname).values()
            try:
                ud=Register.objects.get(email=uname)
            except:
                print("An exception occurred")            
            if userData:
                   userData1=""
                   userData1=Register.objects.filter(password=pwd).values()
                   if  userData1:
                            ud=Register.objects.get(email=uname)
                            print(ud.userRole)
                            bt=ud.userRole
                            uname=ud.Name
                            perm=UserrolePermissions.objects.filter(activity_name="printerjobs").values()
                            if bt=="admin":
                                if(perm[0]['admin']['READ']=="Checked"):
                                    obj = Loginmodel.objects.get(id=2)
                                    detailObj=Loginmodel.objects.filter(id=2).update(loginuname=uname)                     
                                    return  redirect("indexpage")
                                else:
                                     return HttpResponse ("Permission Denied!!!")                    
                            elif bt=="operator":
                                if(perm[0]['operator']['READ']=="Checked"):
                                      obj = Loginmodel.objects.get(id=2)
                                      detailObj=Loginmodel.objects.filter(id=2).update(loginuname=uname)                  
                                      return  redirect("indexpage")                   
                                else:
                                     return HttpResponse ("Permission Denied!!!")  
                            elif bt=="supervisor":
                                if(perm[0]['supervisor']['READ']=="Checked"):
                                      obj = Loginmodel.objects.get(id=2)
                                      detailObj=Loginmodel.objects.filter(id=2).update(loginuname=uname)                     
                                      return  redirect("indexpage")
                                else:
                                     return HttpResponse ("Permission Denied!!!")
                            elif bt=="masterdata":
                                if(perm[0]['masterdata']['READ']=="Checked"):
                                      obj = Loginmodel.objects.get(id=2)
                                      detailObj=Loginmodel.objects.filter(id=2).update(loginuname=uname)                     
                                      return  redirect("indexpage")
                                else:
                                     return HttpResponse ("Permission Denied!!!")                            
                   else:
                      return HttpResponse ("Password is incorrect!!!")
            else:
                  return HttpResponse ("User does not exit")
        else:
          return render(request, 'login.html' )     
def signout_view(request,*args,**kwargs):
        obj = Loginmodel.objects.get(id=2)
        detailObj=Loginmodel.objects.filter(id=2).update(loginuname="") 
        logout(request)
        return redirect("signin")
