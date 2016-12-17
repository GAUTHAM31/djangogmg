from django.contrib import admin
from .models import employee
# Register your models here.
class employeeAdmin(admin.ModelAdmin):
	list_display = ['user','salary','eid','s_leave','c_leave','present']


admin.site.register(employee,employeeAdmin)