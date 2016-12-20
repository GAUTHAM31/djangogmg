from django.contrib import admin
from .models import employee,r_leave
# Register your models here.
class employeeAdmin(admin.ModelAdmin):
	list_display = ['user','salary','eid','s_leave','c_leave','present']
class r_leaveAdmin(admin.ModelAdmin):
	list_display = ['emp_id','date1','date2','l_type','halfday']


admin.site.register(employee,employeeAdmin)
admin.site.register(r_leave,r_leaveAdmin)
