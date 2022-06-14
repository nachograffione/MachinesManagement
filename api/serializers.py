from rest_framework import serializers
from .models import Company, MachineClass, Machine


# SERIALIZERS FOR NON-STORED CLASSES--------------------------------------------
# They use Serializer instead of ModelSerializer

class WorkingDataSerializer(serializers.Serializer):
    data = serializers.DictField()


# SERIALIZERS FOR STORED CLASSES------------------------------------------------

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ["id", "name"]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name"]


class MachineClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineClass
        fields = ["name"]


class MachineSerializer(serializers.ModelSerializer):
    machine_class = MachineClassSerializer()
    company = CompanySerializer()

    class Meta:
        model = Machine
        fields = ["id", "name", "machine_class",
                  "company"]
