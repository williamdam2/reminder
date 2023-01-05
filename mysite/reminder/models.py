from django.db import models
from django.contrib.auth.models import User
from django.db import models

MAC_STATUS_LIST = [
    (0,'NG'),
    (1,'OK'),
    (2,'SETTING')
]

class MachineType(models.Model):
    macType = models.CharField(primary_key=True,max_length=50)

class MachineStatus(models.Model):
    macId = models.CharField(primary_key=True,max_length=50) # Machine ID ex: DCR001
    macType = models.ForeignKey(MachineType,default=None,on_delete=models.SET_DEFAULT) # Machine Type UP/DOWN APS DCR 
    line = models.CharField(max_length=10)
    model = models.CharField(max_length=10)
    status = models.IntegerField(default=1,choices=MAC_STATUS_LIST) # TRUE : OK , FALSE : NG
    buildConfig = models.CharField(max_length=10,null=True,blank=True)
    lotId = models.CharField(max_length=30,default="")
    curDetail = models.CharField(max_length=1000,null=True,blank=True)
    updated = models.DateTimeField(auto_now=True,null=True)
    sw = models.CharField(max_length=30, null=True, blank=True)  
    def __str__(self):
        return self.macId + " - " + self.model

class user_mac(models.Model):
    machine = models.ForeignKey(MachineStatus,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        unique_together =  ('machine','user')
    def __str__(self):
        return self.user.username+"_"+self.machine.macId

    
