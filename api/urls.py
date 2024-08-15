from django.urls import path
from .views import defaultView

urlpatterns = [
    path('',defaultView.as_view()),
]
