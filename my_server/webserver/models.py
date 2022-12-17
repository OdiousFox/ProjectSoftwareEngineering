from django.db import models
# import the models to make tables for the data
# Create your models here.

'''
- Table to store the different types of devices. 
- Ensures that there is no redundancy by not repeating the info in other tables.
'''
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
    entry_hour=models.IntegerField()
    light=models.FloatField()
    temperature=models.FloatField()
    pressure=models.FloatField()

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
    entry_hour=models.IntegerField()
    BatV=models.FloatField()
    Bat_status=models.IntegerField()
    Hum_SHT=models.FloatField()
    #since the Lht devices can either return a ILL_lx or TempC_DS reading the one without a value will be set to null.
    ILL_lx=models.FloatField(default=None,null=True,blank=True)
    TempC_DS=models.FloatField(default=None,null=True,blank=True)
    TempC_SHT=models.FloatField()

#Table for metadata
class Meta_data(models.Model):
    entry_id=models.AutoField(primary_key=True)
    dev_uid=models.CharField(max_length=25)
    gateway_id=models.CharField(max_length=100)
    longitude=models.DecimalField(max_digits=22, decimal_places=16)    # Location longitude
    latitude=models.DecimalField(max_digits=22, decimal_places=16)    # Location latitude
    rssi=models.IntegerField()
    snr=models.FloatField()
    airtime=models.FloatField()


