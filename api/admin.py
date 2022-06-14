from django.contrib import admin
from .models import Company, MachineClass, Machine

admin.site.register(Company)
admin.site.register(MachineClass)
admin.site.register(Machine)
