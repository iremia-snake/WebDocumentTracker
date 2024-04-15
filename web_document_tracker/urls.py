from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from web_document_tracker import views

urlpatterns = [
     path('', views.index, name='home'),
     path('add/', views.AddView, name='add'),
     path('about/', views.about, name='about'),
     path('profile/', views.userpage, name = 'profile'),
     path('logout/', views.logoutMethod, name='link_logout'),
     path('404/', views.error_404_view, name='error404')
]