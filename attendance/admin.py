from django.contrib import admin
from .models import employee,r_leave,public_holidays, admins, managedby,att_record
# Register your models here.
class employeeAdmin(admin.ModelAdmin):
	list_display = ['user','eid','s_leave','c_leave','present','dept']
class r_leaveAdmin(admin.ModelAdmin):
	readonly_field=('no_of_days',)
	list_display = ['emp_id','date1','l_type','reason','l_id','confirmation']
class public_holidaysAdmin(admin.ModelAdmin):
	list_display = ['day']
class adminsAdmin(admin.ModelAdmin):
	list_display = ['user','admin_id']
class managedbyAdmin(admin.ModelAdmin):
    list_display = ['eid','mid']
class att_recordAdmin(admin.ModelAdmin):
    list_display = ['emp_id','date','status','time_in','time_out']

admin.site.register(employee,employeeAdmin)
admin.site.register(r_leave,r_leaveAdmin)
admin.site.register(public_holidays,public_holidaysAdmin)
admin.site.register(admins,adminsAdmin)
admin.site.register(managedby,managedbyAdmin)
admin.site.register(att_record,att_recordAdmin)
