from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import datetime 

# Create your models here.
class employee(models.Model):
	def __unicode__(self):
	 	return  unicode(self.user)
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	eid= models.IntegerField()#employee id
	fname= models.CharField(max_length=20)
	lname=models.CharField(max_length=20)
	c_leave=models.IntegerField(default=15)#casaul leave
	s_leave=models.IntegerField(default=6)#sick_leave
	e_leave=models.IntegerField(default=0)
	present=models.IntegerField(default=0)#daily attendance flag
	elg_c_cre=models.BooleanField(default=False)
	elg_s_cre=models.BooleanField(default=False)
	REQUIRED_FIELDS = ['user', 'eid']
	DEPT_CHOICES = (('BA', 'Business Analysis Team'),('dev', 'Developer'),('QA', 'Quality Team'))
	dept = models.CharField(max_length=3,choices=DEPT_CHOICES,default='BA')
	j_date = models.DateField(default=datetime.date.today)
	t_date = models.DateField(default=datetime.date(2100,1,1))

class managedby(models.Model):
	eid=models.ForeignKey(employee, on_delete=models.CASCADE)
	mid=models.IntegerField();

class r_leave(models.Model):
    emp_id = models.ForeignKey(employee, on_delete=models.CASCADE)
    date1 = models.DateField()#leave period start
    #date2 = models.DateField()#leave period end
    #no_of_days=models.IntegerField(default=0)
    leave_type_choice=(('SL','sick leave'),('CL','Casaul leave'),('EL','Earned Leave'))
    l_type = models.CharField(max_length=10,choices=leave_type_choice,default='CL')
    reason = models.CharField(max_length=100)
    confirmation=models.IntegerField(default=0)
    l_id = models.AutoField(primary_key=True)

class att_record(models.Model):
	emp_id = models.IntegerField()
	date = models.DateField()
	status_type=((-1,'T'),(0,'A'),(1,'P'),(2,'SL'),(3,'CL'),(4,'EL'),(5,'PC'))
	status=models.IntegerField(choices=status_type,default=-1)
	time_in=models.DateTimeField(null=True)
	time_out=models.DateTimeField(null=True)

class log():
    logid=models.AutoField(primary_key=True)
    admin_id = models.IntegerField()
    logdata= models.TextField()


class public_holidays(models.Model):
	day=models.DateField()


class admins	(models.Model):
	def __unicode__(self):
	 	return  unicode(self.user)
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	admin_id=models.AutoField(primary_key=True)
#class team_lead(models.Model):
#	DEPT_CHOICES = (('BA', 'Business Analysis Team'),('dev', 'Developer'),('QA', 'Quality Team'))
#	dept = models.CharField(max_length=3,choices=DEPT_CHOICES,default='BA')
#	email=models.EmailField(max_length=254)
	#id


#create an unatu table

