from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Account, RoomType, Room, Reservation, Service, Refund, Bill, ReservationService


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'name', 'avatar', 'DOB', 'Address', 'phone', 'email', 'sex', 'role',
                  'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account(
            username=validated_data['username'],
            name=validated_data['name'],
            avatar=validated_data.get('avatar'),
            DOB=validated_data.get('DOB'),
            Address=validated_data.get('Address'),
            phone=validated_data.get('phone'),
            email=validated_data.get('email'),
            sex=validated_data.get('sex'),
            role=validated_data.get('role'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['avatar'] = instance.avatar.url
        return req


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'nameRoomType', 'price', 'quantity', 'image', 'active']


class RoomSerializer(serializers.ModelSerializer):
    roomType = serializers.SlugRelatedField(slug_field='nameRoomType', queryset=RoomType.objects.all())

    class Meta:
        model = Room
        fields = ['id', 'nameRoom', 'roomType', 'status', 'active']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'nameService', 'price']


class ReservationServiceSerializer(serializers.ModelSerializer):
    service = serializers.SlugRelatedField(slug_field='nameService', queryset=Service.objects.all())
    price = serializers.CharField(source='service.price')

    class Meta:
        model = ReservationService
        fields = ['service', 'price', 'quantity']


class ReservationSerializer(serializers.ModelSerializer):
    guest = serializers.SlugRelatedField(slug_field='username', queryset=Account.objects.all())
    room = RoomSerializer(many=True)
    services = ReservationServiceSerializer(source='reservationservice_set', many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'guest', 'services', 'room', 'bookDate', 'checkin', 'checkout', 'statusCheckin']

    def update(self, instance, validated_data):
        room_data = validated_data.pop('room', None)
        if room_data:
            for room in room_data:
                room_id = room.get('id')  # Lấy id từ room
                if not room_id:
                    continue  # Nếu không có id, bỏ qua
                try:
                    room_instance = instance.room.get(id=room_id)  # Lấy phòng theo id
                except Room.DoesNotExist:
                    continue  # Nếu phòng không tồn tại, bỏ qua
                room_instance.nameRoom = room.get('nameRoom', room_instance.nameRoom)
                room_instance.save()
        # Cập nhật các trường khác
        instance.statusCheckin = validated_data.get('statusCheckin', instance.statusCheckin)
        instance.save()
        return instance

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

class ReservationDetailSerializer(serializers.ModelSerializer):
    # guest = AccountSerializer()
    guest = serializers.SlugRelatedField(slug_field='username', queryset=Account.objects.all())
    room = RoomSerializer(many=True)
    services = ReservationServiceSerializer(source='reservationservice_set', many=True, read_only=True)

    class Meta:
        model = ReservationSerializer.Meta.model
        fields = ReservationSerializer.Meta.fields + ['services', 'created_date', 'updated_date', 'active']


class RefundSerializer(serializers.ModelSerializer):
    guest = AccountSerializer()
    reservation = ReservationSerializer()

    class Meta:
        model = Refund
        fields = ['id', 'guest', 'reservation', 'LyDo']


class BillSerializer(serializers.ModelSerializer):
    guest = AccountSerializer()
    reservation = ReservationSerializer()

    class Meta:
        model = Bill
        fields = '__all__'