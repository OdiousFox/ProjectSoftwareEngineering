from django.db import models
# import the models to make tables for the data
# Create your models here.

'''
- Table to store the different types of devices. 
- Ensures that there is no redundancy by not repeating the info in other tables.
'''
class DeviceType(models.Model):
    type_id=models.CharField(max_length=25,primary_key=True)
    type_name=models.CharField(max_length=20)
    attributes=models.TextField()
    pass

#Table to keep a record of all devices in use.
'''
- dev_uid is device name and primary field.
- device_type is a foreign key that references type_id in DeviceType table.
- address is the actual location of the devices in use.
'''
class Device(models.Model):
    dev_uid=models.CharField(max_length=25,primary_key=True)
    device_type=models.ForeignKey(DeviceType,on_delete=models.CASCADE)
    address=models.TextField()
    pass


'''
- to remove the redundant 'Null' entries we make two seperate tables since we already know there are two types of devices.
- Each device produces different values.
- dev_uid a foreign key to the Device table will show what table the reading must go into.
- entry_date to keep record of when the reading was done.
- Since all fields can have duplicate entries an auto increment field was added "entry_id" to keep record of the number of records.
'''
#Table for the pycom device entries
class PyEntries(models.Model):
    entry_id=models.AutoField(primary_key=True)
    dev_uid=models.ForeignKey(Device,on_delete=models.CASCADE)
    entry_date=models.DateTimeField()
    light=models.FloatField()
    temperature=models.FloatField()
    pressure=models.FloatField(default=0)
    
#Table for the lht device entries.
class LhtEntries(models.Model):
    entry_id=models.AutoField(primary_key=True)
    dev_uid=models.ForeignKey(Device,on_delete=models.CASCADE)
    entry_date=models.DateTimeField()
    BatV=models.FloatField()
    Bat_status=models.IntegerField()
    Hum_SHT=models.FloatField()
    #since the Lht devices can either return a ILL_lx or TempC_DS reading the one without a value will be set to null.
    ILL_lx=models.FloatField(default=None)
    TempC_DS=models.FloatField(default=None)
    TempC_SHT=models.FloatField()
   



