from django.urls import path
from .views import ContactView,TestimonialView

urlpatterns = [
    path('contact/', ContactView.as_view()),
    path('testimonial/', TestimonialView.as_view()),
]
