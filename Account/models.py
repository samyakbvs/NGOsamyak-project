from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib import auth
from os.path import join as path_join
# Create your models here.

class Site(models.Model):
    Name = models.CharField(max_length=264)
    Address = models.CharField(max_length=1000)
    ThingsNeeded = models.CharField(max_length=1000)
    Picture = models.ImageField(upload_to='images/')
    Description = models.CharField(max_length=1000)
    Phone = models.BigIntegerField()

    def __str__(self):
        return self.Name

    def summary(self):
        return self.Description[:70]

# class CreateHistory(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name='activities')
#     ngo = models.ForeignKey(Site,default=1,on_delete=models.CASCADE)
#     # TempImg = path_join('images', 'personal2.png')
#     # Name = models.CharField(max_length=264,unique=False)
#     # NGO_name = models.CharField(max_length=264)
#     ThingsDonated = models.CharField(max_length=1000)
#     # NGO_image = models.ImageField(default=TempImg,upload_to='images/')
#     Paid = models.BooleanField(default=False)

class Collection(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name='activities')
    ngo = models.ForeignKey(Site,default=1,on_delete=models.CASCADE)
    Paid = models.BooleanField(default=False)
    uid = models.CharField(max_length=264)

class ThingsDonated(models.Model):
    collection = models.ForeignKey(Collection,on_delete=models.CASCADE,default=1,related_name='things')
    name = models.CharField(max_length=264)
    quantity = models.IntegerField()

class Donation(models.Model):
    amount = models.BigIntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    uid = models.CharField(max_length=264)
    succesful = models.BooleanField(default=False)

class MonetaryCollection(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    ngo = models.ForeignKey(Site,default=1,on_delete=models.CASCADE)
    Things = models.CharField(max_length=1000)
    Amount = models.BigIntegerField(default=1)
    Weight = models.BigIntegerField(default=1)
    Paid = models.BooleanField(default=False)
