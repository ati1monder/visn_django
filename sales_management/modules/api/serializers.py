from rest_framework import serializers

class OrderSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=5000)