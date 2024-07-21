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
    quanlity = models.CharField(max_length=10)
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


class Reservation(BaseModel):
    guest = models.ForeignKey(Account, on_delete=models.CASCADE,
                              limit_choices_to={'role': Account.Roles.KhachHang})
    room = models.ManyToManyField(Room, related_name='rooms')
    bookDate = models.DateTimeField()
    checkin = models.DateField()
    checkout = models.DateField()
    active = models.BooleanField(default=True)  # Trường active để quản lý trạng thái đặt phòng

    def __str__(self):
        room_names = ", ".join(self.room.values_list('nameRoom', flat=True))
        return f"{room_names} - Guest: {self.guest.name}"
    #     sẽ trả về một danh sách các tên phòng (nameRoom) của các phòng liên quan đến đối tượng Reservation hiện tại dưới dạng danh sách.
    #     Phương thức join() được sử dụng để kết hợp các tên phòng thành một chuỗi, phân tách bởi dấu phẩy và khoảng trắng (", ").


class Service(BaseModel):
    nameService = models.CharField(max_length=200, null=True)
    price = models.FloatField()

    def __str__(self):
        return str(self.nameService)


# class PhieuNhanPhong(BaseModel):
#     IDPhieuDatPhong = models.ForeignKey(PhieuDatPhong, on_delete=models.CASCADE)
#     DanhSachPhong = models.ManyToManyField(Phong)
#
#     def __str__(self):
#         return f"PhieuNhanPhong {self.phieunhanphong_id} - PhieuDatPhong {self.IDPhieuDatPhong.LoaiPhong}"


class Refund(models.Model):
    guest = models.ForeignKey(Account, null=True, on_delete=models.CASCADE,
                              limit_choices_to={'role': Account.Roles.KhachHang})
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    LyDo = models.TextField()

    def __str__(self):
        return str(self.guest)


class Bill(BaseModel):
    guest = models.ForeignKey(Account, null=True, on_delete=models.CASCADE,
                              limit_choices_to={'role': Account.Roles.KhachHang})
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True)
    services = models.ManyToManyField(Service)
    totalAmount = models.FloatField()
    summary = models.TextField()
    active = models.BooleanField(default=True)

    def calculate_total_amount(self):
        # Tính tổng tiền phòng từ reservation
        room_cost = self.reservation.room.roomType.price

        # Tính tổng chi phí các dịch vụ
        service_cost = sum(service.price for service in self.services.all())

        # Tổng cộng các chi phí
        self.totalAmount = room_cost + service_cost
        self.save()

    def __str__(self):
        return str(self.guest) + " " + str(self.summary) + " " + str(self.totalAmount)