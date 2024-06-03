from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from web_document_tracker import views

urlpatterns = [
     path('', views.index, name='home'),
     path('add/', views.addView, name='add'),
     path('edit/<int:contract_id>/', views.editView, name='edit'),
     path('about/', views.about, name='about'),
     path('profile/', views.userpage, name = 'profile'),
     path('logout/', views.logoutMethod, name='link_logout'),
     path('404/', views.error_404_view, name='error404'),
     path('500/', views.error_500_view, name='error500'),
     path('contract/<int:contract_id>/', views.view_contract, name='view_contract'),
     path('addAjax/',views.addAjax, name='addAjax'),
     path('policity/', views.policy_view, name='policity')
]