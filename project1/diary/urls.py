from django.urls import path, include

from diary.views import home 

urlpatterns = [
    path('', home, name='home'),
]