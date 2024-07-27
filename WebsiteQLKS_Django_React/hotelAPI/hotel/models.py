from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


class BaseModel(models.Model):
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Account(AbstractUser):
    name = models.CharField(max_length=100)
    avatar = CloudinaryField(null=True)
    DOB = models.DateField(null=True)
    Address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)

    class Sex(models.IntegerChoices):
        NAM = 1, 'Nam'
        NU = 2, 'Nữ'

    sex = models.IntegerField(choices=Sex.choices, null=True)

    class Roles(models.IntegerChoices):
        ADMIN = 1, 'Admin'
        LeTan = 2, 'Lễ tân'
        KhachHang = 3, 'Khách hàng'

    role = models.IntegerField(choices=Roles.choices, null=True)

    def __str__(self):
        return self.username


class RoomType(BaseModel):
    nameRoomType = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    quantity = models.CharField(max_length=10)
    image = CloudinaryField()

    def __str__(self):
        return self.nameRoomType


class Room(BaseModel):
    nameRoom = models.CharField(max_length=100)
    roomType = models.ForeignKey(RoomType, on_delete=models.CASCADE)

    # startDate = models.DateField(null=True)
    # endđate = models.DateField(null=True)

    class Status(models.IntegerChoices):
        Trong = 0, 'Trống'
        CoNguoi = 1, 'Có người'

    status = models.IntegerField(choices=Status, default=0)

    def __str__(self):
        return self.nameRoom


class Service(BaseModel):
    nameService = models.CharField(max_length=200, null=True)
    price = models.FloatField()

    def __str__(self):
        return str(self.nameService)


class Reservation(BaseModel):
    guest = models.ForeignKey(Account, on_delete=models.CASCADE,
                              limit_choices_to={'role': Account.Roles.KhachHang})
    room = models.ManyToManyField(Room, related_name='rooms')
    services = models.ManyToManyField(Service, through='ReservationService')
    bookDate = models.DateTimeField()
    checkin = models.DateField()
    checkout = models.DateField()
    active = models.BooleanField(default=True)  # Trường active để quản lý trạng thái đặt phòng
    statusCheckin = models.BooleanField(default=False)

    def __str__(self):
        room_names = ", ".join(self.room.values_list('nameRoom', flat=True))
        return f"{room_names} - Guest: {self.guest.name}"


class ReservationService(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    createdDate = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    # Thêm trường total_price
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.service.nameService} - Reservation: {self.reservation.guest.name}"


class Bill(BaseModel):
    reservation_service = models.ForeignKey(ReservationService, null=True, on_delete=models.CASCADE)
    totalAmount = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)

    def calculate_total_amount(self):
        total_services_cost = sum(rs.total_price for rs in self.reservation_service.reservation.reservationservice_set.all())
        total_days = (self.reservation_service.reservation.checkout - self.reservation_service.reservation.checkin).days
        room_price = sum(room.price for room in self.reservation_service.reservation.room.all())
        total_room_cost = total_days * room_price
        self.totalAmount = total_services_cost + total_room_cost

    def save(self, *args, **kwargs):
        self.calculate_total_amount()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest} - {self.totalAmount}"


class Refund(models.Model):
    guest = models.ForeignKey(Account, null=True, on_delete=models.CASCADE,
                              limit_choices_to={'role': Account.Roles.KhachHang})
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    LyDo = models.TextField()

    def __str__(self):
        return str(self.guest)