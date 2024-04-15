from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.contrib.auth.forms import UserChangeForm
from web_document_tracker.models import *
from datetime import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'никнейм',
            'first_name': 'имя',
            'last_name': 'фамилия',
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['info', 'profile_pic', 'contact']

class DocumentTypeForm(ModelForm):
    class Meta:
        model = DocumentType
        fields = ['name']

class TradingPlatformForm(ModelForm):
    class Meta:
        model = TradingPlatform
        fields = ['name', 'url']

class ContractTypeForm(ModelForm):
    class Meta:
        model = ContractType
        fields = ['name', 'description']

class ExtraDataForm(ModelForm):
    date_range = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'date-range-picker'}), label='продолжительность действия договора')
    class Meta:
        model = ExtraData
        exclude = ['id', 'contract']
        fields = ['date', 'subject', 'price', 'payment_term', 'registration_number']
        widgets = {
            'date': DateInput(),
            'start_date': DateInput(),
            'end_date': DateInput()
        }
        labels = {
            'date': 'дата оформления',
            'subject': 'предмет договора',
            'price': 'цена',
            'payment_term': 'условия оплаты',
            'start_date': 'дата начала действия договора',
            'end_date': 'дата окончания действия договора',
            'registration_number': 'регистрационный номер',

        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        date_range = self.cleaned_data.get('date_range')

        date_start, date_end = date_range.split(' - ')
        print(date_start)
        print(date_end)
        instance.start_date = datetime.strftime(datetime.strptime(date_start,'%d.%m.%Y'), '%Y-%m-%d')
        instance.end_date = datetime.strftime(datetime.strptime(date_end, '%d.%m.%Y'), '%Y-%m-%d')

        if commit:
            instance.save()
        return instance

class CompanyTypeForm(ModelForm):
    class Meta:
        model = CompanyType
        fields = ['name', 'transcription']

class AgentForm(ModelForm):
    class Meta:
        model = Agent
        fields = ['company_name', 'company_type', 'address', 'url', 'tax_number', 'insurance_number']

class AgentDataForm(ModelForm):
    class Meta:
        model = AgentData
        fields = ['last_name', 'middle_name', 'first_name', 'phone_number']

class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ['type', 'trading_platform', 'agent']
        labels = {
            'type' : 'тип документа',
            'trading_platform' : 'платформа',
            'agent': 'контрагент'
        }
    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        empty_field = 'не выбрано'
        self.fields['type'].empty_label = empty_field
        self.fields['trading_platform'].empty_label = empty_field
        self.fields['agent'].empty_label = empty_field

# Определяем inline-форму для модели ExtraData
ExtraDataFormSet = inlineformset_factory(Contract, ExtraData, form=ExtraDataForm, fields=['date', 'subject', 'price', 'payment_term', 'date_range', 'registration_number'])

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['contract', 'type', 'url']