from django.contrib import admin
from .models import employee,r_leave,public_holidays,team_lead
# Register your models here.
class employeeAdmin(admin.ModelAdmin):
	list_display = ['user','salary','eid','s_leave','c_leave','present','dept']
class r_leaveAdmin(admin.ModelAdmin):
	readonly_field=('no_of_days',)
	list_display = ['emp_id','date1','date2','no_of_days','l_type','reason']
class public_holidaysAdmin(admin.ModelAdmin):
	list_display = ['day']
class team_leadAdmin(admin.ModelAdmin):
	list_display=['email','dept']

admin.site.register(employee,employeeAdmin)
admin.site.register(r_leave,r_leaveAdmin)
admin.site.register(public_holidays,public_holidaysAdmin)
admin.site.register(team_lead,team_leadAdmin)
