from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        
        # Check if the combination of username and password already exists
        try:
            user = User.objects.get(username=data['username'])
            if check_password(data['password'], user.password):
                raise serializers.ValidationError("This username and password combination is already registered.")
        except User.DoesNotExist:
            pass  # If the user does not exist, continue with registration
        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
