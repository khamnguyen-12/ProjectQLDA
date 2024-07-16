from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from rest_framework import generics, status, viewsets, parsers, permissions, exceptions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from . import serializers, perm
from .models import Account, RoomType, Room, Reservation, Service, Refund, Bill
from .serializers import (
    AccountSerializer,
    RoomTypeSerializer,
    RoomSerializer,
    ReservationSerializer,
    ServiceSerializer,
    RefundSerializer,
    BillSerializer,
)


class AccountViewSet(viewsets.ViewSet, generics.CreateAPIView,
                     # generics.DestroyAPIView,
                     generics.ListAPIView):
    queryset = Account.objects.filter(is_active=True).all()
    serializer_class = AccountSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]  # upload được hình ảnh và làm việc với json
    permission_classes = [permissions.AllowAny()]  # role nào vô cùng đc

    def get_permissions(self):
        if self.action in ['list', 'get_current_user', 'partial_update']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'account_is_valid']:
            if isinstance(self.request.user, AnonymousUser):
                if self.request.data and (self.request.data.get('role') == str(Account.Roles.KhachHang)):
                    return [permissions.AllowAny()]
                else:
                    return [permissions.IsAuthenticated()]
            elif self.request.data and self.request.data.get('role') == str(Account.Roles.LeTan):
                if self.request.user.role in [Account.Roles.ADMIN.value]:
                    return [permissions.IsAuthenticated()]
                else:
                    raise exceptions.PermissionDenied()
            elif self.request.data and self.request.data.get('role') in [str(Account.Roles.ADMIN)]:
                if self.request.user.role == Account.Roles.ADMIN.value:
                    return [permissions.IsAuthenticated()]
                else:
                    raise exceptions.PermissionDenied()
        elif self.action in ['delete_staff']:
            permission_classes = [perm.IsAdmin()]

    # API xem chi tiết tài khoản hiện (chỉ xem được của mình) + cập nhật tài khoản (của mình)
    # /users/current-user/
    # @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    # def get_current_user(self, request):
    #     # Đã được chứng thực rồi thì không cần truy vấn nữa => Xác định đây là người dùng luôn
    #     # user = user hiện đang đăng nhập
    #     user = request.user
    #     if request.method.__eq__('PATCH'):
    #
    #         for k, v in request.data.items():
    #             # Thay vì viết user.first_name = v
    #             setattr(user, k, v)
    #         user.save()
    #
    #     return Response(serializers.AccountSerializer(user).data)

    @action(detail=False, methods=['GET'], url_path='current-user')
    def get_current_user(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({"detail": "Authentication credentials were not provided."}, status=401)

        serializer = self.serializer_class(user)
        return Response(serializer.data, status=200)


    # API cập nhật một phần cho User
    # @action(methods=['patch'], url_path='patch-current-user', detail=False)
    # def patch_current_user(self, request):
    #     # Đã được chứng thực rồi thì không cần truy vấn nữa => Xác định đây là người dùng luôn
    #     # user = user hiện đang đăng nhập
    #     user = request.user
    #     # Khi so sánh thì viết hoa hết
    #     if request.method.__eq__('PATCH'):
    #
    #         for k, v in request.data.items():
    #             # Thay vì viết user.first_name = v
    #             setattr(user, k, v)
    #         user.save()
    #
    #     return Response(serializers.AccountSerializer(user).data)

    # API vô hiệu hoá tài khoản nhân viên
    # /users/<user_id>/delete-account/
    @action(detail=True, methods=['patch'], url_path='delete-staff')
    def delete_staff(self, request, pk=None):
        user = Account.objects.get(pk=pk)
        user.is_active = False
        user.save()
        return Response({"Thông báo": "Vô hiệu hoá tài khoản thành công."}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], url_path='is_valid', detail=False)
    def account_is_valid(self, request):
        email = self.request.query_params.get('email')
        username = self.request.query_params.get('username')

        if email:
            tk = Account.objects.filter(email=email)
            if tk.exists():
                return Response(data={'is_valid': "True", 'message': 'Email đã tồn tại'}, status=status.HTTP_200_OK)

        if username:
            tk = Account.objects.filter(username=username)
            if tk.exists():
                return Response(data={'is_valid': "True", 'message': 'Username đã tồn tại'},
                                status=status.HTTP_200_OK)

        return Response(data={'is_valid': "False"}, status=status.HTTP_200_OK)


class RoomTypeViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    # pagination_class = RoomTypePaginator

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            if not (self.request.user.is_authenticated and
                    self.request.user.role in Account.Roles.ADMIN.value):  # Chỉ admin mới có quyền
                raise PermissionDenied("Only admin can perform this action.")
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = self.queryset
        q = self.request.query_params.get('nameRoomType')
        if q:
            queryset = queryset.filter(nameRoomType__icontains=q)

        return queryset

    @action(methods=['get'], url_path='rooms', detail=True)
    def get_rooms(self, request, pk):
        lops = self.get_object().room_set.filter(active=True)
        q = request.query_params.get('nameRoom')
        if q:
            lops = lops.filter(nameRoom__icontains=q)

        return Response(serializers.RoomSerializer(lops, many=True).data,
                        status=status.HTTP_200_OK)


class RoomViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    # pagination_class = RoomPaginator

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            if not (self.request.user.is_authenticated and
                    self.request.user.role in Account.Roles.ADMIN.value):  # Chỉ admin mới có quyền
                raise PermissionDenied("Only admin can perform this action.")
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return self.queryset


class ReservationViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_permissions(self):
        if self.action in ['patch_current_reservation', 'partial_update', 'list', 'create']:
            if (self.request.user.is_authenticated and
                    self.request.user.role in Account.Roles.LeTan.value):
                return [permissions.IsAuthenticated()]
            else:
                raise PermissionDenied("Only the customer or receptionists can partially update this reservation.")
        elif self.action == 'get_reservation_guest':
            return [permissions.IsAuthenticated(), perm.IsKhachHang()]
        elif self.action == 'cancel_reservation':
            return [permissions.IsAuthenticated(), self.request.user.role in [Account.Roles.LeTan.value]]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return self.queryset

    def create(self, request, *args, **kwargs):
        customer_id = request.data.get('account')
        room_type_id = request.data.get('roomtype')

        if not customer_id or not room_type_id:
            return Response({'detail': 'Customer ID and Room Type ID are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        rooms = Room.objects.filter(room_type_id=room_type_id, status=0)

        if not rooms.exists():
            return Response({'detail': 'No available rooms for the selected room type.'},
                            status=status.HTTP_400_BAD_REQUEST)

        room = rooms.first()  # Chọn phòng đầu tiên có sẵn

        reservation = Reservation.objects.create(customer_id=customer_id)
        reservation.room.add(room)
        reservation.save()

        room.status = 1  # Cập nhật trạng thái phòng không còn sẵn sàng
        room.save()

        return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)

    # Cập nhật phiếu đặt phòng
    @action(detail=True, methods=['patch'], url_path='current-reservation')
    def patch_current_reservation(self, request, pk=None):
        reservation = request.reservation
        # reservation = self.get_object()
        if request.method.__eq__('PATCH'):

            for k, v in request.data.items():
                setattr(reservation, k, v)
            reservation.save()

        return Response(serializers.ReservationSerializer(reservation).data)

    # Xoá phiếu đặt phòng
    @action(detail=True, methods=['post'], url_path='cancel-reservation')
    def cancel_reservation(self, request, pk=None):
        reservation = self.get_object()
        # if request.user != reservation.customer and not request.user.is_receptionist:
        #     raise PermissionDenied("Only the customer or receptionists can cancel this reservation.")

        # Thực hiện xóa reservation khỏi cơ sở dữ liệu
        reservation.delete()

        return Response({"detail": "Reservation has been cancelled successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], url_path='get-reservation-guest', detail=False)
    def get_reservation_guest(self, request):
        reservations = Reservation.objects.filter(guest=request.user).order_by('-created_date')
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceViewSet(viewsets.ViewSet,
                     generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]


# class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     permission_classes = [IsAuthenticated]


class RefundListCreateView(generics.ListCreateAPIView):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer
    permission_classes = [IsAuthenticated]


class RefundDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer
    permission_classes = [IsAuthenticated]


class BillListCreateView(generics.ListCreateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]


class BillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

# Create your views here.
