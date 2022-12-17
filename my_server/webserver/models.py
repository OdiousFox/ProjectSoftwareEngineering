from django.db import models
# import the models to make tables for the data
# Create your models here.


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
    dev_uid=models.CharField(max_length=25)
    entry_date=models.DateTimeField()
    light=models.FloatField()
    temperature=models.FloatField()
    pressure=models.FloatField(default=0)
    

#Table for the pycom device hourly avgs
class Py_Averages(models.Model):
    entry_id=models.AutoField(primary_key=True)
    dev_uid=models.CharField(max_length=25)
    entry_date=models.IntegerField()
    light=models.FloatField()
    temperature=models.FloatField()
    pressure=models.FloatField(default=0)

#Table for the lht device entries.
class LhtEntries(models.Model):
    entry_id=models.AutoField(primary_key=True)
    dev_uid=models.CharField(max_length=25)
    entry_date=models.DateTimeField()
    BatV=models.FloatField()
    Bat_status=models.IntegerField()
    Hum_SHT=models.FloatField()
    #since the Lht devices can either return a ILL_lx or TempC_DS reading the one without a value will be set to null.
    ILL_lx=models.FloatField(default=None)
    TempC_DS=models.FloatField(default=None)
    TempC_SHT=models.FloatField()
   
#Table for the lht device hourly avgs.
class Lht_Averages(models.Model):
    entry_id=models.AutoField(primary_key=True)
    dev_uid=models.CharField(max_length=25)
    entry_date=models.IntegerField()
    BatV=models.FloatField()
    Bat_status=models.IntegerField()
    Hum_SHT=models.FloatField()
    #since the Lht devices can either return a ILL_lx or TempC_DS reading the one without a value will be set to null.
    ILL_lx=models.FloatField(default=None)
    TempC_DS=models.FloatField(default=None)
    TempC_SHT=models.FloatField()


class MetaData(models.Model):
    entry_id=models.AutoField(primary_key=True)
    entry_date=models.DateTimeField()
    dev_uid=models.CharField(max_length=25)
    BatV=models.FloatField()
    Bat_status=models.IntegerField()
    gateway_uid=models.CharField(max_length=40)
    rssi_val=models.FloatField()
    latitude=models.FloatField()
    longitude=models.FloatField()
    altitude=models.FloatField()
    bandwidth=models.FloatField()
    spreading_factor=models.FloatField()
    frequency=models.FloatField()
    consumed_airtime=models.FloatField()

class MetaAvgs(models.Model):
    entry_id=models.AutoField(primary_key=True)
    entry_date=models.DateTimeField()
    dev_uid=models.CharField(max_length=25)
    BatV=models.FloatField()
    Bat_status=models.IntegerField()
    gateway_uid=models.CharField(max_length=40)
    rssi_val=models.FloatField()
    latitude=models.FloatField()
    longitude=models.FloatField()
    altitude=models.FloatField()
    bandwidth=models.FloatField()
    spreading_factor=models.FloatField()
    frequency=models.FloatField()
    consumed_airtime=models.FloatField()

