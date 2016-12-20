from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class employee(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	salary=models.IntegerField()
	eid= models.IntegerField()#employee id
	c_leave=models.IntegerField()#casaul leave
	s_leave=models.IntegerField()#sick_leave
	present=models.IntegerField()#daily attendance flag
	REQUIRED_FIELDS = ['user', 'eid']

   

class r_leave(models.Model):
    emp_id = models.ForeignKey(employee, on_delete=models.CASCADE)
    date1 = models.DateField()#leave period start
    date2 = models.DateField()#leave period end
    l_type = models.CharField(max_length=10)
    reason = models.CharField(max_length=100)
