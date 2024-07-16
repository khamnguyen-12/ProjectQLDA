from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Account, Refund,
    RoomType, Room, Reservation,
    Service, Bill
)




admin.site.register(Account)
admin.site.register(Refund)
admin.site.register(Bill)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Service)
# Register your models here.
