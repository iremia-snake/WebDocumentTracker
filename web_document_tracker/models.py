from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image

class Profile(models.Model):    # Профиль пользователя. Связан с таблицей пользователей один к одному
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio=models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    facebook = models.CharField(max_length=50, null=True, blank=True)
    twitter = models.CharField(max_length=50, null=True, blank=True)
    instagram = models.CharField(max_length=50, null=True, blank=True)

    @receiver(post_save, sender=User)   # сигнал на создание пользователя
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)   # сигнал на сохранение пользователя
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    def __str__(self):
        return str(self.user)
class DocumentType(models.Model):
    name = models.CharField(max_length=100)
class TradingPlatform(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
class ContractType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
class ExtraData(models.Model):
    date = models.DateTimeField()
    subject = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=14, decimal_places=4)
    payment_term = models.CharField(max_length=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_number = models.CharField(max_length=10)

class CompanyType(models.Model):
    name = models.CharField(max_length=67)
    transcription = models.CharField(max_length=255)
class Agent(models.Model):
    company_name = models.CharField(max_length=67)
    company_type = models.ForeignKey(CompanyType, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    tax_number = models.IntegerField() #max_length=100
    insurance_number = models.IntegerField() #max_length=11
class AgentData(models.Model):
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=18)
class Contract(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(ContractType, on_delete=models.SET_NULL, null=True)
    trading_platform = models.ForeignKey(TradingPlatform, on_delete=models.SET_NULL, null=True)
    extra_data = models.OneToOneField(ExtraData, on_delete=models.SET_NULL, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'Document'

class Document(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True)
    url = models.CharField(max_length=255)
