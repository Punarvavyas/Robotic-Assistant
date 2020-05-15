from django.contrib import admin
from .models import RoboUser,Robot,Location,Admin,Transaction
# Register your models here.
admin.site.register(RoboUser)
admin.site.register(Robot)
admin.site.register(Location)
admin.site.register(Admin)
admin.site.register(Transaction)

