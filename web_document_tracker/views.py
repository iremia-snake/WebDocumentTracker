from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from web_document_tracker.forms import *
from web_document_tracker.forms import EditProfileForm, ProfileForm
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from web_document_tracker.models import *

@login_required
def AddView(request):
    if request.method == "POST":
        contract_form = ContractForm(request.POST)
        extra_data_formset = ExtraDataFormSet(request.POST, instance=Contract())
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
                context={"user": request.user, "contract_form": contract_form, 'extra_data_formset': extra_data_formset}
            )

    else:
        contract_form = ContractForm()
        extra_data_formset = ExtraDataFormSet(instance=Contract())
        return render(
            request = request,
            template_name="web_document_tracker/add_entry.html",
            context={"user": request.user, "contract_form": contract_form, 'extra_data_formset': extra_data_formset}
        )
@login_required
def userpage(request):
    if request.method == "POST":
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
        else:
            messages.error(request, 'Unable to complete request')
        return redirect("profile")

    user_form = EditProfileForm(instance=request.user)
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
@login_required
def index(request):
    elements = [i for i in range(10)]
    for i in Contract.objects.all():
        elements.append(i)
    entries_per_page = 5
    page_number = request.GET.get('page', 1)
    paginator = Paginator(elements, entries_per_page)
    try:
        list = paginator.get_page(page_number)
    except EmptyPage:
        list = paginator.get_page(paginator.num_pages - 1)
    data = {
        'elements' : list,
    }
    return render(request, 'web_document_tracker/index.html', data)

@login_required
def contract_view(request, contract_id = None):
    if request.GET and contract_id:
        return render(request, 'web_document_tracker/', context={Contract.objects.filter(id = contract_id).first()})


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
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, 'web_document_tracker/404.html')
