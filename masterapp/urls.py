from django.contrib import admin
from masterapp import views
from django.urls import path
urlpatterns = [
        # path("printer",views.listprinter,name="printerpage"),
        # path("view/<int:id>",views.Viewprinterview),
        # path('update/<int:id>/', views.updateprinter), 
        # path("stop/<int:id>",views.Viewstopview),
        # path("client/<int:id>",views.Clientview.as_view(),name="client"), 
        # path('printer/<int:id>',views.Viewgetview.as_view(),name="emp-geteditjob"),
        
        path("printer/change/<int:id>",views.Viewprinterview.as_view(),name="emp-editjob"), 
        path("printerstop/change/<int:id>",views.Jobeditstopview.as_view(),name="empstop-editjob"),
        # path('pauseprinter/',views.PausePrinter.as_view(),name="pause"),
        # path('demo/all',views.Demoview.as_view(),name="demo-all"),
        path('pause/<int:id>',views.PauseClassview.as_view(),name="pause-printer"),
        # path('search/',views.Searchview.as_view(),name="search"), 
        # path('squat',views.Runcode.as_view(),name="squat"),
        path('search/', views.searchBar, name='search'),
        path("returnserialget/<int:id>",views.ReturnsnGet.as_view(),name="return-get"),
        path("returnserialno/<int:id>",views.Returnserialnumbers.as_view(),name="return-numbres"),
        
        path("nextserial/<int:id>",views.Nextserialno.as_view(),name="next-numbres"), 
        path('indexpage/', views.listing, name='indexpage'),
        path("home",views.Candidatehomeview.as_view(),name="cand-home"),
        path("scannerhome",views.Scannermessageview.as_view(),name="scanner-message"),
        path("httpalert1",views.HttpAlert1.as_view(),name="httpalert1"),
        path("batchstopmess/",views.Batchstopmessageview.as_view(),name="batch-stop-message"),
        path("printererrors/",views.Errorview.as_view(),name="printer-errors"), 
        path("scannersoftware/",views.Scannersoftwareview.as_view(),name="scanner-software"), 
        path("autovisionopen/<int:id>",views.Autovisionopenview.as_view(),name="autovision"),
        path("grade/",views.Getgradedata.as_view(),name="grade"),
        path("gradecount/<int:id>",views.Gradecount.as_view(),name="gradecount"),
        
        # path("referer/",views.get_referer,name="referer"),
        
        path("signin/",views.Signinview.as_view(),name="signin"),
        path("signout/",views.signout_view,name="signout"),  


        
        path("serialnumberdownload/<int:id>",views.Serialnumberdownloadagainview.as_view(),name="serialnumberdownload"), 
           
 ]           

  