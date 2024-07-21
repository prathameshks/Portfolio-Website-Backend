from django.db import models
from api.models import Visitor

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    visitor_details = models.ForeignKey(Visitor, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.name
    
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    rating = models.IntegerField()
    Visitor_details = models.ForeignKey(Visitor, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.name