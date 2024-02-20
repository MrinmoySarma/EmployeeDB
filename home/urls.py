from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'), 
    path('department', views.getdata, name='getdata'),
    path('department/<int:department_code>', views.department, name='department'),
    path('contact', views.contact, name='contact'), 
]
