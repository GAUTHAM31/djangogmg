from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from attendance.models import employee, r_leave , public_holidays
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from dateutil.parser import parse as parse_date
from django.shortcuts import redirect
import teste
import numpy as np
import datetime 


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
				#usr = User.objects.get(username=username)
				#emp = employee.objects.get(user=usr)
				#return render(request,'attendance/login.html',{'employee':emp})
				return redirect('/home/')
			else:
				return HttpResponse("DISABLED")
		else:
			return render_to_response('attendance/index.html', {}, context)#redirect to invaild  username password url
			#HttpResponse("invaild")
	else:
		return redirect(index)

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
		date_1=parse_date(date_1)
		date_2=parse_date(date_2)
		date_1=datetime.date(date_1.year, date_1.month, date_1.day)
		date_2=datetime.date(date_2.year, date_2.month, date_2.day)
		#to count no of days
		days = np.busday_count( date_1, date_2 )
		holidays=public_holidays.objects.all()
		for holiday in holidays:
			if date_1<holiday.day and date_2>holiday.day:
				if holiday.day.isoweekday()<6:
					days=days-1;
		b=r_leave(emp_id=employee.objects.get(user=request.user),no_of_days=days,date1=date_1,date2=date_2,l_type=ltype,reason=reason1)
		b.save()
		return redirect('/confirmation/')
	else:
		return redirect('/lrequest/')

@login_required
def ladd(request):
	return HttpResponse("email send")
