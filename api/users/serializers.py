from rest_framework import serializers
from api.users.models import User

class AuthenticateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]

class UserSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=255, required=True, allow_blank=False, allow_null=False) # dont use allow null and allow blank both = True
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    is_active = serializers.BooleanField(read_only=True)
    # is_staff = serializers.BooleanField(read_only=True)
    # is_approved = serializers.BooleanField(read_only=True)
    password = serializers.CharField(required=True, write_only=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'role',
            'password'
        ]

    def create(self, validated_data):
        role = self.context.get("role", None)
        if role:
            validated_data['role'] = role
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)  # throws unique email exception here
        user.set_password(password)
        user.is_active = True
        user.is_approved = False
        user.is_superuser = False
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance

    def get_role(self, obj):
        try:
            return obj.role.code
        except:
            return ''