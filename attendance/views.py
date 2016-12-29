from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from attendance.models import employee, r_leave , public_holidays , team_lead
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from dateutil.parser import parse as parse_date
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import teste
import numpy as np
import datetime 
import hashtest


def index(request):
	if request.user.is_authenticated():
		return redirect('/home/')
	else:
		return render(request,'attendance/index.html',{})
	# Create your views here.

def logina(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		
		if user:
			if user.is_active:
				login(request,user)
				return redirect('/home/')
			else:
				return HttpResponse("DISABLED")
		else:
			return render_to_response('attendance/index.html', {}, context)#redirect to invaild  username password url
			#HttpResponse("invaild")
	else:
		return redirect(index)#redirect if not post request was send

@login_required
def home(request):
	emp = employee.objects.get(user=request.user)
	return render(request,'attendance/login.html',{'employee':emp})




@login_required
def l_request(request):
	emp = employee.objects.get(user=request.user)
	return render(request,'attendance/lrequest.html',{'employee':emp})


@login_required
def send(request):
	context = RequestContext(request)
	if request.method == 'POST':
		date_1= request.POST['datef']
		date_2= request.POST['datet']
		ltype= request.POST['type']
		reason1= request.POST['reason']
		#converting date from unicode to date---------------------
		date_1=parse_date(date_1)
		date_2=parse_date(date_2)
		date_1=datetime.date(date_1.year, date_1.month, date_1.day)
		date_2=datetime.date(date_2.year, date_2.month, date_2.day)
		#to count no of days---------------------------------------
		days = np.busday_count( date_1, date_2 )
		holidays=public_holidays.objects.all()
		for holiday in holidays:
			if date_1<holiday.day and date_2>holiday.day:
				if holiday.day.isoweekday()<6:
					days=days-1
		#adding request to database----------------------------------------------------------------
		emp=employee.objects.get(user=request.user)
		b=r_leave(emp_id=emp,no_of_days=days,date1=date_1,date2=date_2,l_type=ltype,reason=reason1)
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
<body>
<div>"""+emp.user.username+" in your team wants "+lt+" to take leave from"+str(date_1)+"to "+str(date_2)+""" 
Attendance Record:"""+str(emp.s_leave)+"    "+str(emp.c_leave)+"  Reason "+reason1+"""
<a href="http://localhost:8000/approve/"""+hash1+"/"+enc1+"""" >
<button class="button button2" name="response">Yes</button></a></div>
<a href="http://localhost:8000/approve/"""+hash0+"/"+enc0+"""" >
<button class="button button2" name="response">No</button></a></div>
</body></html>"""
		to = team_lead.objects.all().filter(dept=emp.dept)
		FROM ='test4generalpurpose@gmail.com'
		for TO in to:
			teste.py_mail("Leave Request", email_content, TO.email, FROM)
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

