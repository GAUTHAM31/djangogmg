from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from attendance.models import employee
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
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
		return render_to_response('attendance/index.html', {}, context)

@login_required
def home(request):
	emp = employee.objects.get(user=request.user)
	return render(request,'attendance/login.html',{'employee':emp})




@login_required
def l_request(request):
	emp = employee.objects.get(user=request.user)
	return render(request,'attendance/lrequest.html',{'employee':emp})

