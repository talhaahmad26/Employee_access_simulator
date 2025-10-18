from rest_framework import serializers

class EmployeeRequestSerializer(serializers.Serializer):
    id = serializers.CharField()
    access_level = serializers.IntegerField()
    request_time = serializers.CharField()  # "HH:MM"
    room = serializers.CharField()

class BulkCheckSerializer(serializers.Serializer):
    data = EmployeeRequestSerializer(many=True)