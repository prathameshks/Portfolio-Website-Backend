from django.db import models

# Create your models here.
class Visitor(models.Model):
    ip_address = models.CharField(max_length=15,blank=True,null=True)
    ip_info = models.JSONField(blank=True,null=True)
    screen_resolution = models.CharField(max_length=15,blank=True,null=True)
    timezone = models.CharField(max_length=50,blank=True,null=True)
    language = models.CharField(max_length=50,blank=True,null=True)
    url = models.CharField(max_length=100,blank=True,null=True)
    user_agent = models.CharField(max_length=100,blank=True,null=True)
    Sec_Ch_Ua = models.CharField(max_length=100,blank=True,null=True)
    Sec_Ch_Ua_Platform = models.CharField(max_length=100,blank=True,null=True)
    Sec_Ch_Ua_Mobile = models.CharField(max_length=100,blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ip_address)