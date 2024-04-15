from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from PIL import Image
from datetime import datetime

class Profile(models.Model):    # Профиль пользователя. Связан с таблицей пользователей один к одному
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    info = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    contact = models.CharField(max_length=50, null=True, blank=True)

    @receiver(post_save, sender=User)   # сигнал на создание пользователя
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)   # сигнал на сохранение пользователя
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    def __str__(self):
        return str(self.user)

@receiver(pre_save, sender=Profile) # сигнал на удаление картинки
def delete_old_profile_pic(sender, instance, **kwargs):
    if not instance.pk:  # Если объект еще не сохранен в базу (новый объект), нечего удалять
        return False

    try:
        old_profile = Profile.objects.get(pk=instance.pk)  # Получаем старый объект из базы
    except Profile.DoesNotExist:
        return False

    if old_profile.profile_pic and instance.profile_pic != old_profile.profile_pic:
        old_profile.profile_pic.delete(save=False)

class DocumentType(models.Model):
    name = models.CharField(max_length=100)
class TradingPlatform(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
class ContractType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name


class CompanyType(models.Model):
    name = models.CharField(max_length=67)
    transcription = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.name
class Agent(models.Model):
    company_name = models.CharField(max_length=67)
    company_type = models.ForeignKey(CompanyType, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    tax_number = models.PositiveIntegerField(null=True, blank=True) #max_length=100
    insurance_number = models.PositiveIntegerField(null=True, blank=True) #max_length=11

    def __str__(self):
        if self.company_type:
            return f'{self.company_type} {self.company_name}'
        return f'{self.company_name}'
class AgentData(models.Model):
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=18)
class Contract(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(ContractType, on_delete=models.SET_NULL, null=True)
    trading_platform = models.ForeignKey(TradingPlatform, on_delete=models.SET_NULL, null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        extra_data = ExtraData.objects.filter(contract_id=self.id).first()
        return f'{self.type} с {self.agent.company_name} за {datetime.strftime(extra_data.date, "%d.%m.%Y")}'
    class Meta:
        managed = True
        db_table = 'Document'

class ExtraData(models.Model):
    date = models.DateTimeField()
    subject = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=14, decimal_places=4, default=0, blank=True)
    payment_term = models.CharField(max_length=500, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_number = models.CharField(max_length=10, null=True, blank=True)
    contract_id = models.OneToOneField(Contract, on_delete=models.SET_NULL, null=True, related_name='extra_data_model')


class Document(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True)
    url = models.CharField(max_length=255)
class UserContract(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE, null=False)