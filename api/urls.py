from django.urls import path
from .views import MachinesApiView, MachineByIdApiView, LastWorkingDataApiView, MachineClassesApiView

urlpatterns = [
    path('machines/', MachinesApiView.as_view()),
    path('machines/<int:id>/', MachineByIdApiView.as_view()),
    path('machines/<int:id>/last-working-data/',
         LastWorkingDataApiView.as_view()),
    path('machine-classes/',
         MachineClassesApiView.as_view()),
]
