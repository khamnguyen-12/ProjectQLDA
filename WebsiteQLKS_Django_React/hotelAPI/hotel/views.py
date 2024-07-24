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
from .models import *
from .serializers import (
    AccountSerializer,
    RoomTypeSerializer,
    RoomSerializer,
    ReservationSerializer,
    ServiceSerializer,
    RefundSerializer,
    BillSerializer, ReservationServiceSerializer,
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
            return [permissions.IsAuthenticated()]
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

    @action(methods=['get'], detail=False, url_path='current_user')
    def get_current_user(self, request):
        # Xác định người dùng đã đăng nhập
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    # API cập nhật một phần cho User
    @action(methods=['patch'], url_path='patch-current-user', detail=False)
    def patch_current_user(self, request):
        # Đã được chứng thực rồi thì không cần truy vấn nữa => Xác định đây là người dùng luôn
        # user = user hiện đang đăng nhập
        user = request.user
        # Khi so sánh thì viết hoa hết
        if request.method.__eq__('PATCH'):

            for k, v in request.data.items():
                # Thay vì viết user.first_name = v
                setattr(user, k, v)
            user.save()

        return Response(serializers.AccountSerializer(user).data)

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


class RoomTypeViewSet(viewsets.ViewSet,
                      generics.ListCreateAPIView,
                      # generics.CreateAPIView
                      ):
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


class ReservationViewSet(viewsets.ViewSet,
                         generics.ListCreateAPIView,
                         generics.ListAPIView,
                         generics.UpdateAPIView
                         ):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    # Chat gpt
    def get_permissions(self):
        if self.action in ['list', 'create']:  # Allow 'list' and 'create' for receptionists
            if self.request.user.is_authenticated and self.request.user.role == Account.Roles.LeTan:
                return [permissions.IsAuthenticated()]
            else:
                raise PermissionDenied("Only receptionists can access this endpoint.")
        elif self.action in ['partial_update', 'update']:
            if self.request.user.is_authenticated and self.request.user.role in [Account.Roles.KhachHang, Account.Roles.LeTan]:
                return [permissions.IsAuthenticated()]
            else:
                raise PermissionDenied("Only the customer or receptionists can partially update this reservation.")
        elif self.action == 'get_reservation_guest':
            return [permissions.IsAuthenticated(), perm.IsKhachHang()]
        elif self.action == 'cancel_reservation':
            if self.request.user.is_authenticated and self.request.user.role in [Account.Roles.LeTan]:
                return [permissions.IsAuthenticated()]
            else:
                raise PermissionDenied("Only receptionists can cancel reservations.")
        return [permissions.AllowAny()]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(active=True)
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset


    def create(self, request, *args, **kwargs):
        guest_name = request.data.get('guest')
        guest = Account.objects.get(username=guest_name)
        room_type_name = request.data.get('room')
        room_data = room_type_name[0]
        roomType = RoomType.objects.get(nameRoomType=room_data.get('roomType'))

        if not guest_name or not room_type_name:
            return Response({'detail': 'Customer ID and Room Type ID are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        rooms = Room.objects.filter(roomType=roomType, status=0)

        if not rooms.exists():
            return Response({'detail': 'No available rooms for the selected room type.'},
                            status=status.HTTP_400_BAD_REQUEST)

        room = rooms.first()  # Chọn phòng đầu tiên có sẵn

        reservation = Reservation.objects.create(
            guest=guest,
            bookDate=request.data.get('bookDate'),  # Cung cấp giá trị cho bookDate
            checkin=request.data.get('checkin'),
            checkout=request.data.get('checkout'),
            active=True  # hoặc các giá trị khác từ request.data
        )
        reservation.room.add(room)
        reservation.save()

        room.status = 1  # Cập nhật trạng thái phòng không còn sẵn sàng
        room.save()

        return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)

    # chat
    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            reservation = self.queryset.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'detail': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role not in [Account.Roles.KhachHang, Account.Roles.LeTan]:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(reservation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['patch'], url_path='deactivate')
    def deactivate_reservation(self, request, pk=None):
        try:
            reservation = self.get_object()
            if request.user.is_authenticated and request.user.role in [Account.Roles.LeTan]:
                reservation.active = False
                reservation.save()
                return Response({'status': 'reservation deactivated'}, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("Only receptionists can deactivate reservations.")
        except Reservation.DoesNotExist:
            return Response({'error': 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)

    #API ghi đè có sẵn (chat)
    # def create(self, request, *args, **kwargs):
    #     serializer = ReservationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     reservation = get_object_or_404(queryset, pk=pk)
    #     serializer = ReservationSerializer(reservation)
    #     return Response(serializer.data)
    #
    # def update(self, request, pk=None):
    #     reservation = get_object_or_404(self.get_queryset(), pk=pk)
    #     serializer = ReservationSerializer(reservation, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #


class ServiceViewSet(viewsets.ViewSet,
                     generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            if not (self.request.user.is_authenticated and
                    self.request.user.role == Account.Roles.LeTan):
                raise PermissionDenied("Only Receptionists can perform this action.")
            return [permissions.IsAuthenticated()]
# class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     permission_classes = [IsAuthenticated]

class ReservationServiceViewSet(viewsets.ViewSet,
                                generics.ListCreateAPIView):
    queryset = ReservationService.objects.all()
    serializer_class = ReservationServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            # Chỉ cho phép người dùng có vai trò 'Lễ tân' sử dụng phương thức 'create'
            if not (self.request.user.is_authenticated and
                    self.request.user.role == Account.Roles.LeTan):
                raise PermissionDenied("Only Receptionists can perform this action.")
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Cũng có thể đặt quyền cho các hành động khác nếu cần
            if not (self.request.user.is_authenticated and
                    self.request.user.role == Account.Roles.Admin):
                raise PermissionDenied("Only Admins can perform this action.")
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    def create(self, request, *args, **kwargs):
        reservation_id = request.data.get('reservationId')
        service_id = request.data.get('service')
        quantity = int(request.data.get('quantity', 1))

        try:
            reservation = Reservation.objects.get(id=reservation_id)
            service = Service.objects.get(id=service_id)
        except (Reservation.DoesNotExist, Service.DoesNotExist):
            return Response({"detail": "Reservation or Service not found."}, status=status.HTTP_404_NOT_FOUND)

        if not reservation.active:
            return Response({"detail": "Reservation is not active."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = service.price * quantity

        reservation_service = ReservationService.objects.create(
            reservation=reservation,
            service=service,
            quantity=quantity,
            total_price=total_price
        )

        serializer = self.get_serializer(reservation_service)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
