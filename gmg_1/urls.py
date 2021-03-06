"""gmg_1 Configuration URL

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include,url
from django.contrib import admin
from attendance import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index),
    url(r'^login/',views.logina),
    url(r'^logintryagain/',views.tryagain),
    url(r'^lrequest/',views.l_request),
    url(r'^home/',views.home),
    url(r'^overview/',views.overview),
    url(r'^delete_submit/',views.deleteselected),
    url(r'^approve_leave/',views.approve_leave),
    url(r'^approve_submit/',views.approveselected),
    url(r'^lrequestConfirmed/',views.send),
    url(r'^confirmation/',views.ladd),
    url(r'^ajax/',views.ajaxview),
    url(r'^ajaxsend/',views.ajaxtest),
    url(r'^logout/',views.logoutf),
    url(r'^adminlogin/',views.adminl),
    url(r'^admins/',views.admincheck),
    url(r'^adminshome/',views.adminhome),
    url(r'^dailyreport/',views.dailyreport),
    url(r'^customreport/',views.customreport),
    url(r'^edituser/',views.edituser),
    url(r'^editsuccess/',views.editsuccess),
    url(r'^adminapprove_leave/',views.adminapprove_leave),
    url(r'^adminapprove_submit/',views.adminapproveselected),
    url(r'^unauthorised/',views.unauthorised),
    url(r'^editunauthorised/',views.editunauthorised),
    url(r'^addotherleave/',views.addotherleave),
    url(r'^addusermain/',views.addusermain),
    url(r'^adduser/',views.adduser),
    url(r'^addusersuccess/',views.addusersuccess),
    url(r'^deletemanager/',views.deletemanager),
    url(r'^editmanager/',views.editmanagers),
    url(r'^addmanager/',views.addmanagers),
    url(r'^logs/',views.viewlogs)
]
