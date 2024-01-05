from django.urls import path
from .views import *

urlpatterns = [
    path('',defaultView.as_view()),
]
