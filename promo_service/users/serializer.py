from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    user_id = serializers.IntegerField(source="id")
