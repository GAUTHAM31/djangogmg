from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from attendance.models import employee, r_leave , public_holidays ,admins, managedby, att_record, editlogs
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from dateutil.parser import parse as parse_date
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import logout
from datetime import timedelta, date
import teste
import numpy as np
import datetime
import hashtest


def index(request):
	if request.user.is_authenticated():
		return redirect(home)
	else:
		return render(request,'attendance/login.html',{})
	# Create your views here.

def logina(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		try:
			empl=employee.objects.get(user=user)
		except employee.DoesNotExist:
			empl=None
		if empl:
			if user.is_active:
				login(request,user)
				return redirect(home)
			else:
				return HttpResponse("DISABLED")
		else:
			return redirect(index)#redirect to invaild  username password url
			#HttpResponse("invaild")
	else:
		return redirect(index)#redirect if not post request was send

@login_required
def home(request):
    try:
        emp = employee.objects.get(user=request.user)
    except employee.DoesNotExist:
        emp=None
    slt=r_leave.objects.filter(l_type='SL').filter(emp_id=emp).count()
    clt=r_leave.objects.filter(l_type='CL').filter(emp_id=emp).count()
    elt=r_leave.objects.filter(l_type='EL').filter(emp_id=emp).count()
    if emp:
        return render(request,'attendance/home.html',{'fname':emp.fname,'lname':emp.lname,'sl':emp.s_leave,'cl':emp.c_leave,'el':emp.e_leave,'slt':slt,'clt':clt,'elt':elt})
    else:
        return redirect(adminhome)

@login_required
def overview(request):
    try:
        emp = employee.objects.get(user=request.user)
    except employee.DoesNotExist:
        return redirect(adminhome)
    if emp:
        rl = list(r_leave.objects.filter(emp_id=emp))
        return render(request,'attendance/overview.html',{'rlist':rl})

@login_required
def approve_leave(request):
    try:
        emp = employee.objects.get(user=request.user)
        ml = list(managedby.objects.filter(mid=emp.eid))
        rl = list()
        for item in ml:
            l1 = list(r_leave.objects.filter(emp_id=item.eid).filter(confirmation=0))
            rl.extend(l1)
        return render(request,'attendance/approve_leave.html',{'rlist':rl})
    except employee.DoesNotExist:
        return redirect(adminhome)
@login_required
def approveselected(request):
    if request.method == 'POST':
       lrid= request.POST['l_id']
       rlobj=r_leave.objects.get(l_id=lrid)
       rlobj.confirmation=1
       rlobj.save()
       return redirect(approve_leave)


@login_required
def l_request(request):
    try:
	    emp = employee.objects.get(user=request.user)
	    return render(request,'attendance/lrequest.html',{'employee':emp})
    except employee.DoesNotExist:
        return redirect(adminhome)


@login_required
def send(request):
	context = RequestContext(request)
	if request.method == 'POST':
		date_1= request.POST['datef']
		#date_2= request.POST['datet']
		ltype= request.POST['type']
		reason1= request.POST['reason']
		#converting date from unicode to date---------------------
		date_1=parse_date(date_1)
		#date_2=parse_date(date_2)
		date_1=datetime.date(date_1.year, date_1.month, date_1.day)
		#date_2=datetime.date(date_2.year, date_2.month, date_2.day)
		#to count no of days---------------------------------------
		#days = np.busday_count( date_1, date_2 )
		#holidays=public_holidays.objects.all()
		#for holiday in holidays:
			#if date_1<holiday.day and date_2>holiday.day:
				#if holiday.day.isoweekday()<6:
					#days=days-1
		#adding request to database----------------------------------------------------------------
		emp=employee.objects.get(user=request.user)
		b=r_leave(emp_id=emp,date1=date_1,l_type=ltype,reason=reason1)
		b.save()
		#making temp url--------------------------------------------
		hash1, enc1 = hashtest.encode_data([emp.eid,b.l_id,1])
		hash0, enc0 = hashtest.encode_data([emp.eid,b.l_id,2])
		#for removing symbols
		enc1=enc1.replace("=","equal")
		enc0=enc0.replace("=","equal")
		enc1=enc1.replace("+","addition")
		enc0=enc0.replace("+","addition")
		enc1=enc1.replace("/","backslash")
		enc0=enc0.replace("/","blackslash")
		enc1=enc1.replace("?","question")
		enc0=enc0.replace("?","question")

		#sending email to team lead--------------------------------
		if ltype=='CL':
			lt="casual leave"
		else:
			lt="sick leave"
		email_content = """
<html>
<head>
<style>
.button {
    background-color: #4CAF50; /* Green */
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
}

.button2 {background-color: #008CBA;}
</style>
</head>
<body>Attendance Record:"""+str(emp.s_leave)+"    "+str(emp.c_leave)+"  Reason "+reason1+"""
<a href="http://localhost:8000/approve/"""+hash1+"/"+enc1+"""" >
<button class="button button2" name="response">Yes</button></a></div>
<a href="http://localhost:8000/approve/"""+hash0+"/"+enc0+"""" >
<button class="button button2" name="response">No</button></a></div>
</body></html>"""
        #add default email here if necessary
		to = managedby.objects.all().filter(eid=emp)
		FROM ='test4generalpurpose@gmail.com'
		for TO in to:
			mm=employee.objects.get(eid=TO.mid)
			teste.py_mail("Leave Request", email_content, mm.user.email, FROM)
		return redirect('/confirmation/')
	else:
		return redirect('/lrequest/')

@login_required
def ladd(request):
	return HttpResponse("email send")

def approval(request,hash,enc):
	enc=enc.replace("equal","=")
	enc=enc.replace("addition","+")
	enc=enc.replace("backslash","/")
	enc=enc.replace("question","?")
	d=hashtest.decode_data(hash, enc)
	emp=employee.objects.get(eid=d[0])
	leave=r_leave.objects.get(l_id=d[1])
	leave.confirmation=d[2]
	leave.save()
	return HttpResponse("confirmation recorded")

@login_required
def logoutf(request):
	logout(request)
	return redirect(index)



#-----------------------------------------------------------------------------------------------------
#------------------------------------------ADMIN VIEW-------------------------------------------------
#-----------------------------------------------------------------------------------------------------


def adminl(request):
	return render(request,'attendance/adminlogin.html',{})

def admincheck(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		try:
			admin=admins.objects.get(user=user)
		except admins.DoesNotExist:
			admin=None
		if admin:
			login(request,user)
			return redirect(adminhome)#put redirect home address for admin later
		else:
			return redirect(adminl)

	else:
			return redirect(adminl)#put correct redirect later
@login_required(login_url='/admins/')
def adminhome(request):
    try:
        admin = admins.objects.get(user=request.user)
        return render(request,'attendance/adminhome.html',{})
    except admins.DoesNotExist:
        return redirect(home)

@login_required(login_url='/adminlogin/')
def dailyreport(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    if request.method == 'POST':
       dailyatt = list(att_record.objects.filter(date=request.post['date']))
       return render(request,'attendance/dailyreport.html',{'dalist':dailyatt})
    else:
       dailyatt = list()
       return render(request,'attendance/dailyreport.html',{'dalist':dailyatt})

@login_required(login_url='/adminlogin/')
def dailyreport(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    if request.method == 'POST':
       date1=request.POST['datef']
       #converting date from unicode to date---------------------
       date1=parse_date(date1)
       date1=datetime.date(date1.year, date1.month, date1.day)
       dailyatt = list(att_record.objects.filter(date=date1))
       return render(request,'attendance/dailyreport.html',{'dalist':dailyatt})
    else:
       dailyatt = list()
       return render(request,'attendance/dailyreport.html',{'dalist':dailyatt})



@login_required(login_url='/adminlogin/')
def customreport(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    dayatt=list()
    if request.method == 'POST':
        date1=request.POST['datef']
        date2=request.POST['datet']
        #converting date from unicode to date---------------------
        date1=parse_date(date1)
        date2=parse_date(date2)
        date1=datetime.date(date1.year, date1.month, date1.day)
        date2=datetime.date(date2.year, date2.month, date2.day)
        #to count no of days---------------------------------------

        customattlist=list()
        def daterange(start_date, end_date):
            for n in range(int ((end_date - start_date).days)):
                yield start_date + timedelta(n)

        #for DATE in daterange(date1, date2):
        #samples = Sample.objects.filter(sampledate__gte=datetime.date(2011, 1, 1),
                                #sampledate__lte=datetime.date(2011, 1, 31))
        dayatt1=att_record.objects.all().filter(date__gte=date1)
        dayatt=dayatt1.filter(date__lte=date2)
            #dayatt=list(dayatt1)
            #customattlist.append(dayatt)
        return render(request,'attendance/customreport.html',{'clist':dayatt})
    else:
        customattlist=list()
        return render(request,'attendance/customreport.html',{'clist':dayatt})
@login_required(login_url='/adminlogin/')
def addusermain(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
	return render(request,'attendance/adduser.html',{})

@login_required(login_url='/adminlogin/')
def edituser(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    details=list()
    if request.method=='POST':
        eid=request.POST['eid']
        details=employee.objects.get(eid=eid)

        return render(request,'attendance/edituser.html',{'det':details})
    else:
        return render(request,'attendance/edituser.html',{'det':details})

@login_required(login_url='/adminlogin/')
def editsuccess(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    rm=request.POST
    eid=rm['eid']
    fn=rm['fn']
    ln=rm['ln']
    jd=rm['jd']
    td=rm['td']
    email=rm['email']
    date1=parse_date(jd)
    date2=parse_date(td)
    date1=datetime.date(date1.year, date1.month, date1.day)
    date2=datetime.date(date2.year, date2.month, date2.day)
    emp=employee.objects.get(eid=eid)
    emp.fname=fn
    emp.lname=ln
    #emp.dept=d
    emp.j_date=date1
    emp.t_date=date2
    emp.user.email=email
    emp.save();
    return render(request, 'attendance/editsuccess.html',{})

@login_required(login_url='/adminlogin/')
def adminapprove_leave(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    l1 = list(r_leave.objects.filter(confirmation=0))
    return render(request,'attendance/adminapproveleave.html',{'rlist':l1})


@login_required(login_url='/adminlogin/')
def adminapproveselected(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    if request.method == 'POST':
       lrid= request.POST['l_id']
       rlobj=r_leave.objects.get(l_id=lrid)
       rlobj.confirmation=1
       rlobj.save()
       #if rlobj.l_type =='CL':
       # rlobj.emp_id.c_leave=rlobj.emp_id.c_leave-1
       #elif rlobj.l_type == 'SL':
       # rlobj.emp_id.s_leave=rlobj.emp_id.s_leave-1
       #else:
       # rlobj.emp_id.e_leave=rlobj.emp_id.e_leave-1
       #rlobj.emp_id.save()
       return redirect(adminapprove_leave)

@login_required(login_url='/adminlogin/')
def unauthorised(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    ulist=att_record.objects.filter(status=0)
    return render(request,'attendance/unauthorised.html',{'ulist':ulist})

def insertlog(admin_id,logdata,logdate):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    new_log= editlogs(admin_id=admin_id,logdata=logdata,logdate=logdate)
    new_log.save()

@login_required(login_url='/adminlogin/')
def editunauthorised(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    if request.method == 'POST':
       flag=1
       eid= request.POST['emp_id']
       admin_id=admins.objects.get(user=request.user).admin_id
       logdate=datetime.datetime.now()
       reason1= request.POST['reason1']
       date= request.POST['date']
       date1=parse_date(date)
       date1=datetime.date(date1.year, date1.month, date1.day)
       status= int(request.POST['status'])
       arobj=att_record.objects.filter(emp_id=eid).get(date=date1)
       arobj.status=status
       arobj.save()
       rlobj=employee.objects.get(eid=eid)
       if status==3:
        rlobj.c_leave=rlobj.c_leave-1
        logdata='Alloted casual leave to'+employee.objects.get(eid=eid).fname+' on '+date
        ltype='CL'
       elif status == 2:
        rlobj.s_leave=rlobj.s_leave-1
        logdata='Alloted sick leave to'+employee.objects.get(eid=eid).fname+' on '+date
        ltype='SL'
       elif status == 4:
        rlobj.e_leave=rlobj.e_leave-1
        logdata='Alloted earned leave to'+employee.objects.get(eid=eid).fname+' on '+date
        ltype='EL'
       else:
        flag=0
        logdata='Corrected absence to present for '+employee.objects.get(eid=eid).fname+' on '+date
       insertlog(admin_id,logdata,logdate)
       if flag == 1:
            b=r_leave(emp_id=rlobj,date1=date1,l_type=ltype,reason=reason1,confirmation=1)
            b.save()
       rlobj.save()
       return redirect(unauthorised)

@login_required(login_url='/adminlogin/')
def addotherleave(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    if request.method == 'POST':
        eid=request.POST['eid']
        jd=request.POST['date1']
        td=request.POST['date2']
        date1=parse_date(jd)
        date2=parse_date(td)
        date1=datetime.date(date1.year, date1.month, date1.day)
        date2=datetime.date(date2.year, date2.month, date2.day)
        reason=request.POST['reason']
        #loop from date1 to date2
        while date1 <= date2:
            emp=employee.objects.get(eid=eid)
            b=r_leave(emp_id=emp,date1=date1,l_type='OL',reason=reason,confirmation=1)
            b.save()
            date1 += datetime.timedelta(days=1)
        return redirect(adminhome)
    else:
        return render(request,'attendance/otherleave.html',{})

@login_required(login_url='/adminlogin/')
def adduser(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    if request.method == 'POST':
        query_dict = request.POST
        eid= query_dict['eid']
        username = query_dict['username']
        email = query_dict['email']
       	password = query_dict['password']
       	fname=query_dict['fname']
       	lname=query_dict['lname']
       	#read rest of the inputs
        new_user = User.objects.create_user(username,email,password)
        new_user.save()
        emp=User.objects.get(username=username)
        p=employee(user=emp,fname=fname,lname=lname,eid=eid)
        p.save()
        return redirect(addusersuccess)
    else:
    	return redirect(addusermain)


@login_required(login_url='/adminlogin/')
def addusersuccess(request):
	return HttpResponse("success")

@login_required(login_url='/adminlogin/')
def editmanagers(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    manlist=list()
    if request.method == 'POST':
        user=request.POST['emp_id']
        details=employee.objects.get(eid=user)
        managers=list(managedby.objects.filter(eid=employee.objects.get(eid=user)))
        for item in managers:
            ml=list(employee.objects.filter(eid=item.mid))
            manlist.extend(ml)
        return render(request,'attendance/editmanager.html',{'manlist':manlist,'eid':user})
    else:
        return render(request,'attendance/editmanager.html',{'det':manlist,})


@login_required(login_url='/adminlogin/')
def deletemanager(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    if request.method == 'POST':
        mid=request.POST['mid']
        eid=request.POST['eid']
        managedby.objects.filter(eid=employee.objects.filter(eid=eid)).filter(mid=mid).delete()
        return redirect(editmanagers)

@login_required(login_url='/adminlogin/')
def addmanagers(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    if request.method=='POST':
        eid=request.POST['eid']
        mid=request.POST['mid']
        p=managedby(eid=employee.objects.get(eid=eid),mid=mid)
        p.save()
    return render(request,'attendance/addmanager.html',{})



@login_required(login_url='/adminlogin/')
def editsuccess(request):
    try:
        admin = admins.objects.get(user=request.user)
    except admins.DoesNotExist:
        return redirect(home)
    rm=request.POST
    eid=rm['eid']
    fn=rm['fn']
    ln=rm['ln']
    jd=rm['jd']
    td=rm['td']#add handlers to remove dependencies for the employee that was deleted like removing him from managers
    email=rm['email']
    date1=parse_date(jd)
    date2=parse_date(td)
    date1=datetime.date(date1.year, date1.month, date1.day)
    date2=datetime.date(date2.year, date2.month, date2.day)
    emp=employee.objects.get(eid=eid)
    emp.fname=fn
    emp.lname=ln
    #emp.dept=d
    emp.j_date=date1
    emp.t_date=date2
    emp.user.email=email
    emp.save();
    return render(request, 'attendance/editsuccess.html',{})




@login_required(login_url='/admins/')
def viewlogs(request):
    try:
        admin = admins.objects.get(user=request.user)
        loglist=list(editlogs.objects.filter())
        return render(request,'attendance/logs.html',{'loglist':loglist})
    except admins.DoesNotExist:
        return redirect(home)
