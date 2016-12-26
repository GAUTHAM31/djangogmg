from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class employee(models.Model):
	def __unicode__(self):
	 	return  unicode(self.user)
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	salary=models.IntegerField()
	eid= models.IntegerField()#employee id
	c_leave=models.IntegerField()#casaul leave
	s_leave=models.IntegerField()#sick_leave
	present=models.IntegerField()#daily attendance flag
	REQUIRED_FIELDS = ['user', 'eid']
	DEPT_CHOICES = (('BA', 'Business Analysis Team'),('dev', 'Developer'),('QA', 'Quality Team'))
	dept = models.CharField(max_length=3,choices=DEPT_CHOICES,default='BA')

   

class r_leave(models.Model):
    emp_id = models.ForeignKey(employee, on_delete=models.CASCADE)
    date1 = models.DateField()#leave period start
    date2 = models.DateField()#leave period end
    no_of_days=models.IntegerField(default=0)
    leave_type_choice=(('SL','sick leave'),('CL','Casaul leave'))
    l_type = models.CharField(max_length=10,choices=leave_type_choice,default='CL')
    reason = models.CharField(max_length=100)
    confirmation=models.IntegerField(default=0)


class public_holidays(models.Model):
	day=models.DateField()

class team_lead(models.Model):
	DEPT_CHOICES = (('BA', 'Business Analysis Team'),('dev', 'Developer'),('QA', 'Quality Team'))
	dept = models.CharField(max_length=3,choices=DEPT_CHOICES,default='BA')
	email=models.EmailField(max_length=254)
