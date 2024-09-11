from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "A senha deve ter pelo menos 6 caracteres."
            )
        return value

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
        ]
        depth = 1
        read_only_fields = ["id"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="Esse e-mail já existe.",
                    )
                ]
            },
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="Esse nome de usuário já existe.",
                    )
                ]
            },
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True, required=True)
    password = serializers.CharField(max_length=127, write_only=True, required=True)
