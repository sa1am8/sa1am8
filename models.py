from django.db import models

# Create your models here.


class ContactInfo(models.Model):
    contact_name = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=20, default='')


class Meta: 
    ordering = ["-my_field_name"]

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        return self.field_name