from django.urls import path
from .views import defaultView, healthView

urlpatterns = [
    path('health/', healthView.as_view()),
    path('',defaultView.as_view()),
]
