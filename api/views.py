from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Machine, Company, MachineClass
from .serializers import MachineSerializer, WorkingDataSerializer, MachineClassSerializer, CompanySerializer


# CLASSES ----------------------------------------------------------------------

class MachinesApiView(APIView):
    def get(self, request):
        # extract the query params
        name_include = request.query_params.get('nameInclude')
        machine_class_name_include = request.query_params.get(
            'machineClassInclude')
        is_working = request.query_params.get('isWorking')

        # filter by name_include and machine_class_name_include
        q = Q()
        if(name_include is not None):
            q = q | Q(name__icontains=name_include)
        if(machine_class_name_include is not None):
            q = q | Q(machine_class__name__icontains=machine_class_name_include)
        machines = Machine.objects.filter(q)

        # filter by is_working
        #   (this is a manual and ugly filtering that should be improved
        #   using Django's things)
        if(is_working is not None):
            valid_value = None
            if(is_working == "true"):
                valid_value = True
            elif (is_working == "false"):
                valid_value = False
            if(valid_value is not None):
                valid_ids = []
                for machine in machines:
                    machine.update_last_working_data()
                    if (machine.is_working() == valid_value):
                        valid_ids.append(machine.id)
                machines = Machine.objects.filter(id__in=valid_ids)
            else:
                return Response({"error": "isWorking must be 'true' or 'false'"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MachineSerializer(machines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # extract the params
        name = request.data.get('name')
        company_name = request.data.get('company')
        machine_class_name = request.data.get('machineClass')

        # check name
        if(name is None):
            return Response({"error": "name must be defined"}, status=status.HTTP_400_BAD_REQUEST)

        # check company_name
        if(company_name is None):
            return Response({"error": "company must be defined"}, status=status.HTTP_400_BAD_REQUEST)

        # check machine_class_name
        if(machine_class_name is None):
            return Response({"error": "machineClass must be defined"}, status=status.HTTP_400_BAD_REQUEST)

        # check if machine_class is valid
        if(machine_class_name is not None):
            machine_class = get_machine_class(machine_class_name)
            if (machine_class is not None):
                machine_class = machine_class
            else:
                # the error data follows the serializer.errors format
                return Response({"error": "machineClass value doesn't exist. Check them with GET /api/machine-classes/"}, status=status.HTTP_400_BAD_REQUEST)

        # retrieve or create the company
        if(company_name is not None):
            company = retrieve_or_create_company(company_name)

        # create the machine
        machine = Machine(name=name, company=company,
                          machine_class=machine_class)
        machine.save()

        # serialize and return
        serializer = MachineSerializer(machine)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MachineByIdApiView(APIView):
    def get(self, request, id):
        try:
            machine = Machine.objects.get(id=id)
            serializer = MachineSerializer(machine)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        # extract the params
        name = request.data.get('name')
        company_name = request.data.get('company')
        machine_class_name = request.data.get('machineClass')

        # retrieve the machine
        try:
            machine = Machine.objects.get(id=id)
            serializer = MachineSerializer(machine)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        # check if machine_class is valid
        if(machine_class_name is not None):
            machine_class = get_machine_class(machine_class_name)
            if (machine_class is not None):
                machine.machine_class = machine_class
            else:
                return Response({"error": "machineClass value doesn't exist. Check them with GET /api/machine-classes/"}, status=status.HTTP_400_BAD_REQUEST)

        # retrieve or create the company
        if(company_name is not None):
            machine.company = retrieve_or_create_company(company_name)

        # update the machine
        if (name is not None):
            machine.name = name
        machine.save()

        # serialize and return
        serializer = MachineSerializer(machine)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            machine = Machine.objects.get(id=id)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        machine.delete()
        return Response(
            {"res": "Object deleted!"}, status=status.HTTP_200_OK)


class LastWorkingDataApiView(APIView):
    def get(self, request, id):
        try:
            machine = Machine.objects.get(id=id)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        machine.update_last_working_data()
        serializer = WorkingDataSerializer(machine.last_working_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MachineClassesApiView(APIView):
    def get(self, request):
        machine_classes = MachineClass.objects.all()
        serializer = MachineClassSerializer(machine_classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# FUNCTIONS --------------------------------------------------------------------

def get_machine_class(machine_class_name):
    try:
        machine_class = MachineClass.objects.get(
            name=machine_class_name)
        serializer = MachineClassSerializer(machine_class)
    except:
        return None
    return machine_class


def retrieve_or_create_company(company_name):
    try:
        company = Company.objects.get(name=company_name)
        serializer = CompanySerializer(company)
    except:
        company = Company(name=company_name)
        company.save()
    return company
