from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from os.path import join as path_join
from django.contrib import auth
# Create your models here.
class Register(models.Model):
    TempImg = path_join('images', 'personal2.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    UserImage = models.ImageField(default=TempImg,upload_to='images/')
    Email = models.EmailField(unique=True)
    FullName = models.CharField(default="Default name", max_length = 1000)
    Address = models.CharField(max_length = 1000)
    Phone = models.BigIntegerField(validators=[MinValueValidator(1000000000)])
    OTP = models.BigIntegerField(default=2048)
    IsVerified = models.BooleanField(default=False)
    def summary(self):
        if len(self.Address) < 20:
            return self.Address
        return self.Address[:20]
