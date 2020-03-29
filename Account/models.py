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

class CreateHistory(models.Model):
    TempImg = path_join('images', 'personal2.png')
    Name = models.CharField(max_length=264,unique=False)
    NGO_name = models.CharField(max_length=264)
    ThingsDonated = models.CharField(max_length=1000)
    NGO_image = models.ImageField(default=TempImg,upload_to='images/')
    Paid = models.BooleanField(default=False)

class Collection(models.Model):
    user = models.CharField(max_length=264)
    User_Address = models.CharField(max_length=1000)
    User_Phone = models.BigIntegerField(validators=[MinValueValidator(1000000000)])
    NGO = models.CharField(max_length=264)
    NGO_Address = models.CharField(max_length=264)
    Things = models.CharField(max_length=1000)
    Donation_Type = models.CharField(max_length=264,default='None')
    Paid = models.BooleanField(default=False)

class MonetaryCollection(models.Model):
    user = models.CharField(max_length=264)
    User_Address = models.CharField(max_length=1000)
    User_Phone = models.BigIntegerField(validators=[MinValueValidator(1000000000)])
    NGO = models.CharField(max_length=264)
    NGO_Address = models.CharField(max_length=264)
    Things = models.CharField(max_length=1000)
    Amount = models.BigIntegerField(default=1)
    Weight = models.BigIntegerField(default=1)
    Paid = models.BooleanField(default=False)
