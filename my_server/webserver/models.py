from django.db import models

# Create your models here.
class DeviceType(models.Model):
    type_id=models.CharField(max_length=25,primary_key=True)
    type_name=models.CharField(max_length=20)
    attributes=models.TextField()
    pass

class Device(models.Model):
    dev_uid=models.CharField(max_length=25,primary_key=True)
    device_type=models.ForeignKey(DeviceType,on_delete=models.CASCADE)
    address=models.TextField()
    pass

class PyEntries(models.Model):
    entry_id=models.AutoField(primary_key=True)
    dev_uid=models.ForeignKey(Device)
    entry_date=models.DateTimeField()
    light=models.FloatField()
    temperature=models.FloatField()

class LhtEntries(models.Model):
    entry_id=models.AutoField(primary_key=True)
    dev_uid=models.ForeignKey(Device)
    entry_date=models.DateTimeField()
    BatV=models.FloatField()
    Bat_status=models.IntegerField()
    Hum_SHT=models.FloatField()
    ILL_lx=models.FloatField()
    TempC_SHT=models.FloatField()
    Work_mode=models.TextField()
    


