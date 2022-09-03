from .views import upgrade_me
from django.urls import path

urlpatterns = [

    path('upgrade/', upgrade_me, name = 'upgrade')
]