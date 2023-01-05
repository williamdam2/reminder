from django.urls import path
from . import views

urlpatterns = [
    path('',views.view_reminder,name="reminder"),
    path('user_add_machine',views.view_userAddMachine,name="userAddMachine"),
    path('logSystem',views.view_logSystem,name="logSystem"),
    path("test", views.view_test, name="test"),
    path('createMachine',views.create_machine,name="createMachine"),
    
    #api
    path('api/getMachineStatus_multi',views.getMachineStatus_multi,name="getMachineStatus_multi"),
    path('api/updateMachineStatus',views.updateMachineStatus,name="updateMachineStatus"),
    path('api/userAddMachineInterest',views.userAddMachineInterest,name="userAddMachineInterest"),
    path('api/userDeleteMachineInterest',views.userDeleteMachineInterest,name="userDeleteMachineInterest"),
    path('api/downloadMachineLog',views.downloadMachineLog,name="downloadMachineLog"),
    
]  