from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
import requests


# NON-STORED CLASSES------------------------------------------------------------

class WorkingData:
    def __init__(self, data=None):
        self.data = data


# MODELS FOR STORED CLASSES-----------------------------------------------------

class Company(SafeDeleteModel):
    # id is created automatically

    # it's unique (see the constraint below)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Companies"
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                condition=models.Q(deleted__isnull=True),
                name='company_unique_non_deleted_name'
            ),
        ]


class MachineClass(SafeDeleteModel):
    # id is created automatically

    # it's unique (see the constraint below)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "MachineClasses"
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                condition=models.Q(deleted__isnull=True),
                name='machine_class_unique_non_deleted_name'
            ),
        ]


class Machine(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # non-stored field
        self.last_working_data = WorkingData()

    # id is created automatically

    # it's unique (see the constraint below)
    name = models.CharField(max_length=50)

    machine_class = models.ForeignKey(MachineClass, on_delete=models.RESTRICT)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "Machines"
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                condition=models.Q(deleted__isnull=True),
                name='machine_unique_non_deleted_name'
            ),
        ]

    def update_last_working_data(self):
        try:
            response = requests.get(
                f"https://wrk.acronex.com/api/challenge/last/{self.id}").json()
            self.last_working_data = WorkingData(response)
            return True
        except:
            return False

    def is_working(self):
        if(self.last_working_data is not None):
            velocity = float(
                self.last_working_data.data['Operación']['Velocidad'].split()[0])
            if(velocity == 0.0):
                return False
            else:
                return True
        return None
