from rest_framework import serializers
from .models import Account, RoomType, Room, Reservation, Service, Refund, Bill


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'name', 'avatar', 'DOB', 'Address', 'phone', 'email', 'sex', 'role']
        extra_kwargs = {'password': {'write_only': True},
                        'role': {'default': 3}
                        }

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
            role=validated_data.get('role', 3),
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
        fields = ['id', 'nameRoomType', 'price', 'quanlity', 'image', 'created_date', 'updated_date', 'active']


class RoomSerializer(serializers.ModelSerializer):
    roomType = serializers.CharField(source='roomType.nameRoomType')

    class Meta:
        model = Room
        fields = ['id', 'nameRoom', 'roomType', 'status', 'created_date', 'updated_date', 'active']


class ReservationSerializer(serializers.ModelSerializer):
    #guest = AccountSerializer()
    guest = serializers.CharField(source='guest.username')
    room = RoomSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ['id', 'guest', 'room', 'bookDate', 'checkin', 'checkout', 'created_date', 'updated_date', 'active']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'nameService', 'price', 'created_date', 'updated_date', 'active']


class RefundSerializer(serializers.ModelSerializer):
    guest = AccountSerializer()
    reservation = ReservationSerializer()

    class Meta:
        model = Refund
        fields = ['id', 'guest', 'reservation', 'LyDo']


class BillSerializer(serializers.ModelSerializer):
    guest = AccountSerializer()
    reservation = ReservationSerializer()
    service = ServiceSerializer(many=True)

    class Meta:
        model = Bill
        fields = '__all__'
