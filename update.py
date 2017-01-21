import os,sys,django
sys.path.append(os.path.join(os.path.dirname(__file__), '/root/gmg_1'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gmg_1.settings")
from django.conf import settings
from django.db import models
django.setup()
from django.contrib.auth.models import User
from attendance.models import employee,public_holidays,att_record,r_leave
from dateutil.parser import parse as parse_date
from django.utils import timezone
import datetime
import urllib,json

#------------------Code----------------------------------------------------
employee.objects.all().update(present=0)#sets all absent at first
today=datetime.date(2016,11,02)#today
days=public_holidays.objects.all()
for d in days:
	if(today==d.day):
		exit(0)
if(today.weekday()<5):
	url="http://192.168.2.180:4373/api/sgTimeCard/Timecard?iEmpId=&dtFrom="+str(today.strftime("%m/%d/%y"))+"&dtTo="+str(today.strftime("%m/%d/%y"))
	response=urllib.urlopen(url)
	resputf8=response.read().decode('utf-8')
	data=json.loads(resputf8)
	for dat in data['sResult']:
		edata=dat['cmpId']
		status=dat['DayType']
		edata=int(edata)
		emp=employee.objects.all()
		try:
			emp=employee.objects.get(eid=edata)
		except employee.DoesNotExist:
			print "can't find "+str(edata)
		if (status=="Absent"):
				l_check=r_leave.objects.filter(date1=today).filter(emp_id=emp).distinct()
				print l_check
				if l_check.exists():
					if(l_check[0].confirmation==1):
						if(l_check[0].l_type=='SL'):
							lvalue=2
							empsl=emp.s_leave
							print empsl
							emp.s_leave=empsl-1
							emp.save()
						elif(l_check[0].l_type=='CL'):
							lvalue=3
							empcl=emp.c_leave
							print empcl-1
							emp.c_leave=empcl-1
							emp.save()
						elif(l_check[0].l_type=='EL'):
							lvalue=4
							empel=emp.e_leave
							print empel-1
							emp.e_leave=empel-1
							emp.save()
						att=att_record(emp_id=edata,date=today,status=lvalue)
						att.save()
				else:
					att=att_record(emp_id=edata,date=today,status=0)#,time_in=timezone.make_aware(timein, timezone.get_current_timezone()),time_out=timezone.make_aware(timeout, timezone.get_current_timezone()))
					att.save()
			
			

		else:
			timin=dat['InTime']
			timein=parse_date(timin)
			timout=dat['OutTime']
			timeout=parse_date(timout)
			att=att_record(emp_id=edata,date=today,status=1,time_in=timezone.make_aware(timein, timezone.get_current_timezone()),time_out=timezone.make_aware(timeout, timezone.get_current_timezone()))
			att.save()

		


#loop to parse excel file
#for row in range(2, sheet.max_row + 1):
#	employee.objects.all().filter(eid=sheet['B'+str(row)].value).update(present=1)



	

 
