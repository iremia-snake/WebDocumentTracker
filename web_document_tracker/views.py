import sys

import django

from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import JsonResponse, HttpResponse

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from django.core import serializers
from django.core.paginator import Paginator, EmptyPage

from web_document_tracker.forms import *

from django.db.models import Q
import json

def is_ajax(request: django.http.request.HttpRequest) -> bool:
    return (
        request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or request.accepts("application/json")
    )



@login_required
def addAjax(request):
    if request.method == 'POST':
        form = TradingPlatformForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            platforms = TradingPlatform.objects.all()
            platform_list = serializers.serialize('json', platforms)
            return addView(request.GET)
        else:
            return JsonResponse({'form errors': form.errors}, status=400)
    return error_404_view(request)

@login_required
def addView(request):
    if request.method == "POST":
        contract_form = ContractForm(request.POST)
        extra_data_formset = ExtraDataFormSet(request.POST, instance=Contract())
        platform_form = PlatformForm(request.POST)
        if contract_form.is_valid() and extra_data_formset.is_valid():
            new_contract = contract_form.save()
            extra_data_formset.instance = new_contract
            extra_data_formset.save()

            messages.success(request, 'Запись успешно добавлена!')
            return redirect('home')
        else:
            messages.error(request, 'Произошла ошибка при сохранении формы. Пожалуйста, исправьте ошибки в форме.')
            return render(
                request, template_name="web_document_tracker/add_entry.html",
                context={
                    "user": request.user,
                    "contract_form": contract_form,
                    'extra_data_formset': extra_data_formset,
                    "platform_form" : platform_form
                }
            )
    else:
        contract_form = ContractForm()
        extra_data_formset = ExtraDataFormSet(instance=Contract())
        platform_form = PlatformForm()

        return render(
            request = request,
            template_name="web_document_tracker/add_entry.html",
            context={
                "user": request.user,
                "contract_form": contract_form,
                "extra_data_formset": extra_data_formset,
                "platform_form" : platform_form
            }
        )
@login_required
def editView(request, contract_id):
    contract_instance = get_object_or_404(Contract, id=contract_id)
    if request.method == "POST":
        contract_form = ContractForm(request.POST, instance=contract_instance)
        extra_data_formset = ExtraDataFormSet(request.POST, instance=contract_instance)
        if contract_form.is_valid() and extra_data_formset.is_valid():
            contract_form.save()
            extra_data_formset.save()
            messages.success(request, 'Информация успешно обновлена!')
            return redirect('home')
        else:
            contract_errors = contract_form.errors
            extra_data_errors = extra_data_formset.errors
            messages.error(request, 'Произошла ошибка при сохранении формы. Пожалуйста, исправьте ошибки в форме.'+'c:'+str(contract_errors)+'  e:'+str(extra_data_errors))
    else:
        contract_form = ContractForm(instance=contract_instance)
        extra_data_formset = ExtraDataFormSet(instance=contract_instance)

    return render(
        request=request,
        template_name="web_document_tracker/edit_entry.html",
        context={
            "user": request.user,
            "contract_form": contract_form,
            "extra_data_formset": extra_data_formset,
        }
    )

@login_required
def userpage(request):
    if request.method == "POST":
        user_form = AdavancedUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
        else:
            messages.error(request, 'Unable to complete request')
        return redirect("profile")

    user_form = AdavancedUserChangeForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    return render(
        request=request,
        template_name="web_document_tracker/user_profile.html",
        context={'request': request, 'user': request.user, "user_form": user_form, "profile_form": profile_form}
    )
@login_required
def about(request):
    phones = (
        {'phone': '8(914) 141-56-98', 'state' : 'програмист'},
        {'phone': '8(914) 487-31-10', 'state' : 'администратор сайта'}
    )
    data = {'phones' : phones}
    return render(request, 'web_document_tracker/about.html', data)

def search(queryset:set, search_query:str) -> set:
    if search_query:
        search_query_lower = search_query.lower()
        queryset = queryset.filter(
            Q(type__name__icontains=search_query_lower) |
            Q(agent__company_name_lower__icontains=search_query_lower) |
            Q(trading_platform__name_lower__icontains=search_query_lower)
        )
    return queryset
@login_required
def index(request):
    elements = Contract.objects.all()
    search_form = SearchForm(request.GET)
    filter_form = CombinedFilterForm(request.GET)

    if filter_form.is_valid():
        contract_types = filter_form.cleaned_data['contract_types_field']
        if len(contract_types):
            elements = elements.filter(type__in=contract_types)
        date_range = filter_form.cleaned_data['date_range']
        if date_range:
            date_start, date_end = date_range.split(' - ')
            start_date = datetime.strftime(datetime.strptime(date_start, '%d.%m.%Y'), '%Y-%m-%d')
            end_date = datetime.strftime(datetime.strptime(date_end, '%d.%m.%Y'), '%Y-%m-%d')
            elements = elements.filter(extra_data_model__date__gte=start_date, extra_data_model__date__lte=end_date)

    if search_form.is_valid():
        search_query = search_form.cleaned_data['search_query']
        elements = search(elements, search_query)

    entries_per_page = 5
    page_number = request.GET.get('page', 1)
    paginator = Paginator(elements, entries_per_page)
    try:
        list = paginator.get_page(page_number)
    except EmptyPage:
        list = paginator.get_page(paginator.num_pages - 1)
    data = {
        'elements' : list,
        'search_form': SearchForm(request.GET),
        'filter_form': CombinedFilterForm(request.GET)
    }
    return render(request, 'web_document_tracker/index.html', data)

@login_required
def view_contract(request, contract_id):
    contract = Contract.objects.get(id=contract_id)
    return render(request, 'web_document_tracker/view_contract.html', {'contract': contract})

def policy_view(request):
    return render(request, 'web_document_tracker/politice.html')


# @login_required
# def contract_view(request, contract_id = None):
#     if request.GET and contract_id:
#         return render(request, 'web_document_tracker/', context={Contract.objects.filter(id = contract_id).first()})
#     else:
#         return HttpResponse('none')


class CustomLoginView(LoginView):
    template_name='registration/login.html'
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()

def logoutMethod(request):
    logout(request)
    return redirect('login')


def error_404_view(request, exception = None):
    return render(request, 'web_document_tracker/404.html')

def error_500_view(request):
    try:
        context = {}
        # ltype, lvalue, ltraceback = sys.exc_info()
        # context = {'type': ltype, 'value': lvalue, 'traceback': ltraceback}
        return render(request, 'web_document_tracker/500.html', context)
    except:
        return HttpResponse('Ошибка на странице ошибки. Позвоните админу.')
